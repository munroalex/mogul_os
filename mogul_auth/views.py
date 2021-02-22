from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User

from esi.clients import EsiClientProvider
from esi.decorators import single_use_token

esi = EsiClientProvider()

# Create your views here.
def home_view(request,*args, **kwargs):
	#return HttpResponse("<h1>Hello World!</h1>")

	return render(request, "home.html")

@single_use_token(scopes=['publicData'])
def login_view(request,token):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		# Let's look up the user in the database
		try:
			loginuser = User.objects.get(username=token.character_name)
		except User.DoesNotExist:
			# Let's create the user
			loginuser = User.objects.create_user(username=token.character_name,email=str(token.character_id) + '@eve.ccp', password=token.character_owner_hash)
		except:
			return redirect('/')
		# Let's finally log in
		user = authenticate(username=token.character_name, password=token.character_owner_hash)
		if user is not None:
			login(request, user)
		else:
			HttpResponse("You probably changed accounts, didn't you?")
		return redirect('/')

def logout_view(request,*args, **kwargs):
	if request.user.is_authenticated:
		logout(request)
		return redirect('/')
	else:
		return redirect('/')