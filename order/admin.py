from django.contrib import admin
from order.models import Address,Order,OrderLine
# Register your models here.

admin.site.register(Address)
# admin.site.register(Order)
admin.site.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('order_id','basic_amount','shipping_charge')
admin.site.register(OrderLine)

