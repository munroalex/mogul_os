# mogul_backend/dynamic_preferences_registry.py

from dynamic_preferences.types import BooleanPreference, StringPreference,DecimalPreference,ChoicePreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.registries import user_preferences_registry
from mogul_backend.serializers import PercentagePreference
import decimal

# we create some section objects to link related preferences together
general = Section('general')
notifications = Section('notifications')
trade = Section('trade')
preference = Section('preference')

# We start with a global preference
@global_preferences_registry.register
class SiteTitle(StringPreference):
    section = general
    name = 'title'
    default = 'Mogul OS'
    required = True

@user_preferences_registry.register
class OrderNotificationsEnabled(BooleanPreference):
    section = notifications
    name = 'order_notifications_enabled'
    default = True
    help_text = 'Would you like to be alerted on order completion?'

@user_preferences_registry.register
class BuyBroker(PercentagePreference):
    section = trade
    name = 'buy_broker'
    default = decimal.Decimal(0.05)
    help_text = 'The buy broker fee you usually pay. Typically 1\% in a structure'

@user_preferences_registry.register
class SellBroker(PercentagePreference):
    section = trade
    name = 'sell_broker'
    default = decimal.Decimal(0.05)
    help_text = 'The sell broker fee you usually pay. Typically 1\% in a structure'

@user_preferences_registry.register
class SalesTax(PercentagePreference):
    section = trade
    name = 'sales_tax'
    default = decimal.Decimal(0.05)
    help_text = 'The sales tax you usually pay. Usually 2.25 with max skills'

@user_preferences_registry.register
class DefaultHub(ChoicePreference):
    choices = [
        ('jita', 'Jita'),
        ('amarr', 'Amarr'),
        ('rens', 'Rens'),
        ('hek', 'Hek'),
        ('dodixie', 'Dodixie'),
        ('stacmon', 'Stacmon'),
    ]
    section = trade
    name = 'default_hub'
    default = "Jita"
    help_text = 'The default trade hub for market graphs'

@user_preferences_registry.register
class LeaderboardEnable(BooleanPreference):
    section = preference
    name = 'leaderboard_enabled'
    default = False
    help_text = 'Would you like to be shown in the leaderboard?'