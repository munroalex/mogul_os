from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.db import models

from esi.clients import EsiClientProvider
from esi.decorators import single_use_token,token_required,tokens_required
from esi.models import Token
from django.core import serializers
from mogul_auth.serializers import EsiCharacterTransactions
from mogul_backend.tasks import importtransactions
from eveuniverse.models import EveType

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
    refer = 'http://localhost:3000/'
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
    refer = 'http://localhost:3000/login'
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
