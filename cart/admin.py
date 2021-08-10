from django.contrib import admin

# Register your models here.
from cart.models import Cart,CartLine

admin.site.register(Cart)
admin.site.register(CartLine)