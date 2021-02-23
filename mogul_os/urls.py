"""mogul_os URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from mogul_auth import views as AuthViews

from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from mogul_auth.viewsets import UserViewSet, TokenViewSet
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'tokens', TokenViewSet,basename="get_queryset")

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^sso/', include('esi.urls', namespace='esi')),

    path('login/', AuthViews.login_view, name="login"),
    path('logout/', AuthViews.logout_view, name="logout"),
    re_path(r'^api/v1/', include(router.urls)), 
    path('link/trade_character', AuthViews.trade_token_view, name="character_trade"),

    path('api/live/transactions', AuthViews.live_transactions, name="live_transactions"),
]
