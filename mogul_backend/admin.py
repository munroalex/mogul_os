from django.contrib import admin
from .models import Transaction,Order,Character
from eveuniverse.models import EveType
from subscriptions import models as submodels

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(Character)
admin.site.register(submodels.SubscriptionPlan)
admin.site.register(submodels.PlanCost)
admin.site.register(submodels.UserSubscription)
admin.site.register(submodels.PlanList)
admin.site.register(submodels.PlanListDetail)