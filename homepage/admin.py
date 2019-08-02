from django.contrib import admin
from .models import Items, Reviews, UserBalance, UserCart, ReturnList
# Register your models here.

admin.site.register(Items)
admin.site.register(Reviews)
admin.site.register(UserBalance)
admin.site.register(UserCart)
admin.site.register(ReturnList)