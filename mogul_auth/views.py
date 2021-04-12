from django.shortcuts import render, redirect,get_object_or_404
from django_discord_connector.models import DiscordClient, DiscordToken, DiscordUser
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse,JsonResponse
from django.template import loader
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.db import models

from esi.clients import EsiClientProvider
from esi.decorators import single_use_token,token_required,tokens_required
from esi.models import Token,CallbackRedirect
from django.core import serializers
from mogul_auth.serializers import EsiCharacterTransactions
from mogul_backend.tasks import importtransactions
from eveuniverse.models import EveType
from django.contrib import messages
from django.urls import reverse
import base64
import requests
import json
import discord
from mogul_backend.DiscordConnector import DiscordConnector
from requests_oauthlib import OAuth2Session
import logging

logger = logging.getLogger(__name__)

esi = EsiClientProvider(spec_file='mogul_auth/swagger.json')

# Create your views here.
def home_view(request,*args, **kwargs):
    #return HttpResponse("<h1>Hello World!</h1>")

    return render(request, "home.html")

@single_use_token(scopes=['publicData'])
def login_view(request,token):
    print(request.META)
    refer = '/'

    if request.user.is_authenticated:
        return redirect(refer)
    else:
        # Let's look up the user in the database
        try:
            loginuser = User.objects.get(username=token.character_name)
        except User.DoesNotExist:
            # Let's create the user
            loginuser = User.objects.create_user(username=token.character_name,email=str(token.character_id) + '@eve.ccp', password=token.character_owner_hash)
        except:
            return redirect(refer)
        # Let's finally log in
        user = authenticate(username=token.character_name, password=token.character_owner_hash)
        if user is not None:
            login(request, user)
        else:
            HttpResponse("You probably changed accounts, didn't you?")
        return redirect(refer)

def logout_view(request,*args, **kwargs):
    refer = 'http://localhost:8000/'
    if request.user.is_authenticated:
        logout(request)
        return redirect(refer)
    else:
        return redirect(refer)

def user_details(request,*args, **kwargs):
    return HttpResponse("You got the deets!");
    #return JsonResponse(request.user)

@token_required(scopes=["esi-wallet.read_character_wallet.v1",'esi-skills.read_skills.v1','esi-assets.read_assets.v1','esi-markets.read_character_orders.v1','esi-universe.read_structures.v1','esi-search.search_structures.v1','esi-markets.structure_markets.v1'],new=True)
def trade_token_view(request,token):
    refer = 'http://localhost:8000/login'
    return redirect("/")

@token_required(scopes=["esi-wallet.read_corporation_wallets.v1",'esi-skills.read_skills.v1','esi-assets.read_assets.v1','esi-markets.read_corporation_orders.v1','esi-universe.read_structures.v1','esi-search.search_structures.v1','esi-markets.structure_markets.v1'],new=True)
def trade_token_corp_view(request,token):
    refer = 'http://localhost:8000/login'
    return redirect("/")

def live_transactions(request,*args, **kwargs):
    character_id = request.GET.get('character_id');
    importtransactions.delay(character_id, request.user.id)
    return HttpResponse("Started pull")

def eve_type(request):
    type_id = int(request.GET.get('type_id'))
    item, returned = EveType.objects.get_or_create_esi(id=type_id)
    data = {
        'name': item.name,
        'volume': item.volume,
    }
    return JsonResponse(data, safe=False)
    return HttpResponse(item)


def sso_callback(request):
    try:
        discord_client = DiscordClient.get_instance()
    except:
        messages.warning(
            request, "The site administrator has not added the Discord Client to the admin panel.")
        return redirect('dashboard')
    data = {
        "client_id": discord_client.client_id,
        "client_secret": discord_client.client_secret,
        "grant_type": "authorization_code",
        "code": request.GET['code'],
        "redirect_uri": discord_client.callback_url,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post('%s/oauth2/token' %
                      discord_client.api_endpoint, data, headers)
    r.raise_for_status()

    json = r.json()
    token = json['access_token']
    me = requests.get('https://discordapp.com/api/users/@me',
                      headers={'Authorization': "Bearer " + token}).json()
    join = requests.post(discord_client.invite_link, headers={
                         'Authorization': "Bearer " + token}).json()
    # Catch errors
    if DiscordToken.objects.filter(discord_user__external_id=me['id']).exists():
        discord_token = DiscordToken.objects.get(discord_user__external_id=me['id'])
        if discord_token.user != request.user:
            messages.error(request, "That Discord user is claimed by another user.")
            return redirect('/')
    if not me['email']:
        messages.add_message(
            request, messages.ERROR, 'Could not find an email on your Discord profile. Please make sure your not signed in as a Guest Discord user.')
        return redirect('/')
    if me['email'] != request.user.email:
        messages.add_message(
            request, messages.WARNING, 'You linked a Discord account with a mismatched email, please verify you linked the correct Discord account.'
        )


    # Delete old token if exists
    if DiscordToken.objects.filter(user=request.user).exists():
        discord_token = request.user.discord_token
        discord_token.delete()

    # Get or Create Discord User
    discord_user = DiscordUser.objects.get_or_create(external_id=me['id'])[0]
    discord_user.username = me['username'] + "#" + me['discriminator']
    if 'nick' in me:
        discord_user.nickname = me['nick'] + "#" + me['discriminator']

    discord_user.save()

    # Attach DiscordToken to user
    dtoken = DiscordToken(
        access_token=json['access_token'],
        refresh_token=json['refresh_token'],
        discord_user=discord_user,
        user=request.user
    )
    dtoken.save()

    sendinvitepost = requests.post(f"http://discordapp.com/api/guilds/{discord_client.server_id}/members/{me['id']}", headers={
                         'Authorization': "Bearer " + token}).json()



    # Let's also do some cool things like creating the user dm channel preference
    disc = DiscordConnector.get_instance()
    channel = disc.initiate_dm(discord_user.external_id)
    channel = channel.json()
    request.user.preferences['notifications__discord_dm_channel'] = channel['id']

    # Okay, let's also send the user a DM
    request.user.dm_user("Welcome to Mogul OS! You have been invited to the Discord Server")


    return JsonResponse(channel, safe=False)

    return redirect('/')

def sso_redirect(request, scopes=None, return_to=None):
    """
    Generates a :model:`esi.CallbackRedirect` for the specified request.
    Redirects to EVE for login.
    Accepts a view or URL name as a redirect after SSO.
    """
    logger.debug(
        "Initiating redirect of %s session %s",
        request.user,
        request.session.session_key[:5] if request.session.session_key else '[no key]'
    )
    if scopes is None:
        scopes = list()
    elif isinstance(scopes, str):
        scopes = list([scopes])

    # ensure only one callback redirect model per session
    if request.session.session_key:
        CallbackRedirect.objects\
            .filter(session_key=request.session.session_key).delete()

    # ensure we have a session
    if not request.session.exists(request.session.session_key):
        logger.debug("Creating new session before redirect.")
        request.session.create()

    if return_to:
        url = reverse(return_to)
    else:
        url = request.get_full_path()

    oauth = OAuth2Session(
        app_settings.ESI_SSO_CLIENT_ID,
        redirect_uri=app_settings.ESI_SSO_CALLBACK_URL,
        scope=scopes
    )
    redirect_url, state = oauth.authorization_url(app_settings.ESI_OAUTH_LOGIN_URL)

    CallbackRedirect.objects.create(
        session_key=request.session.session_key, state=state, url=url
    )
    logger.debug(
        "Redirecting %s session %s to SSO. Callback will be redirected to %s",
        request.user,
        request.session.session_key[:5],
        url
    )
    return redirect(redirect_url)


def receive_callback(request):
    """
    Parses SSO callback, validates, retrieves :model:`esi.Token`,
    and internally redirects to the target url.
    """
    # make sure request has required parameters
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    try:
        assert code
        assert state
    except AssertionError:
        logger.debug("Missing parameters for code exchange.")
        return HttpResponseBadRequest()

    callback = get_object_or_404(
        CallbackRedirect, state=state, session_key=request.session.session_key
    )
    token = Token.objects.create_from_request(request)
    callback.token = token
    callback.save()
    logger.debug(
        "Processed callback for %s session %s. Redirecting to %s",
        request.user,
        request.session.session_key[:5],
        callback.url
    )
    return redirect(callback.url)


def select_token(request, scopes='', new=False):
    """
    Presents the user with a selection of applicable tokens for the requested view.
    """

    @tokens_required(scopes=scopes, new=new)
    def _token_list(r, tokens):
        # Single Scope as string will break the Parser in the template
        if isinstance(scopes, str):
            scopes_output = [scopes]
        else:
            scopes_output = scopes

        # fake distint on character_name to not show duplicates
        # MySQL doesn't support distint on field.
        token_output = []
        _characters = set()
        for t in tokens:
            if t.character_name in _characters:
                continue
            token_output.append(t)
            _characters.add(t.character_name)

        context = {
            'tokens': token_output,
            'scopes': scopes_output
        }

        return render(r, 'esi/select_token.html', context=context)

    return _token_list(request)
