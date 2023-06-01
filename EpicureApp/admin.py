from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Contact)
admin.site.register(UsersInfo)
admin.site.register(Restaturant)
admin.site.register(FoodItem)
admin.site.register(Orders)
admin.site.register(ItemWiseOrders)