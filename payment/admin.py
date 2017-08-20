from django.contrib import admin
from payment.models import *
# Register your models here.
# 
admin.site.register(WxUser, admin.ModelAdmin)
admin.site.register(Order, admin.ModelAdmin)

admin.site.register(OrderData, admin.ModelAdmin)