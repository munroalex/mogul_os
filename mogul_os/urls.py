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
from mogul_backend.viewsets import TransactionViewSet, OrderViewSet, CharacterViewSet,NotificationViewSet,GlobalPreferencesViewSet,StockViewSet,ProfitViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import notifications.urls
from dynamic_preferences.users.viewsets import UserPreferencesViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Mogul OS Api",
      default_version='v1',
      description="MogulOS Application API",
      terms_of_service="https://www.mogulos.com",
      contact=openapi.Contact(email="jeronica@tackledinbelt.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserViewSet, basename="user")
router.register(r'tokens', TokenViewSet,basename="tokens")
router.register(r'transactions', TransactionViewSet, basename="transactions")
router.register(r'characters', CharacterViewSet, basename="characters")
router.register(r'orders', OrderViewSet, basename="orders")
router.register(r'messages', NotificationViewSet, basename="messages")
router.register(r'global', GlobalPreferencesViewSet, basename='global')
router.register(r'preferences', UserPreferencesViewSet, basename='preferences')
router.register(r'profit', ProfitViewSet, basename="profit")
router.register(r'stock', StockViewSet, basename="stock")

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^sso/', include('esi.urls', namespace='esi')),

    path('login/', AuthViews.login_view, name="login"),
    path('logout/', AuthViews.logout_view, name="logout"),
    re_path(r'^api/v1/', include(router.urls)), 
    path('link/trade_character', AuthViews.trade_token_view, name="character_trade"),
    path('link/trade_corp', AuthViews.trade_token_corp_view, name="corp_trade"),

    path('api/live/transactions', AuthViews.live_transactions, name="live_transactions"),
    path('api/live/item', AuthViews.eve_type, name="eve_item"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

