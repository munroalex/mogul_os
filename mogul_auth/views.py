from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

from esi.clients import EsiClientProvider
from esi.decorators import single_use_token,token_required,tokens_required
from esi.models import Token
from django.core import serializers

esi = EsiClientProvider(spec_file='mogul_auth/swagger.json')

# Create your views here.
def home_view(request,*args, **kwargs):
    #return HttpResponse("<h1>Hello World!</h1>")

    return render(request, "home.html")

@single_use_token(scopes=['publicData'])
def login_view(request,token):
    print(request.META)
    refer = 'http://localhost:3000/login'

    if request.user.is_authenticated:
        return redirect(refer)
    else:
        # Let's look up the user in the database
        try:
            loginuser = User.objects.get(username=token.character_name)
        except User.DoesNotExist:
            # Let's create the user
            loginuser = User.objects.crete_user(username=token.character_name,email=str(token.character_id) + '@eve.ccp', password=token.character_owner_hash)
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
    refer = 'http://localhost:3000/'
    if request.user.is_authenticated:
        logout(request)
        return redirect(refer)
    else:
        return redirect(refer)

def user_details(request,*args, **kwargs):
    return HttpResponse("You got the deets!");
    #return JsonResponse(request.user)

@token_required(scopes=["esi-wallet.read_character_wallet.v1",'esi-skills.read_skills.v1','esi-assets.read_assets.v1','esi-markets.read_character_orders.v1'])
def trade_token_view(request,token):
    print(request.META)
    refer = 'http://localhost:3000/login'
    return redirect(refer)

def live_transactions(request,*args, **kwargs):
    character_id = request.GET.get('character_id');
    required_scopes = ['esi-wallet.read_character_wallet.v1']
    token = Token.get_token(character_id, required_scopes)
    try:
        result = esi.client.Wallet.get_characters_character_id_wallet_transactions(
            # required parameter for endpoint
            character_id = character_id,
            # provide a valid access token, which wil be refresh the token if required
            token = token.valid_access_token()
        ).results()
    except HTTPNotFound:
            print("error getting transactions")
    item = result
    print(item)
    return JsonResponse(item , safe=False)