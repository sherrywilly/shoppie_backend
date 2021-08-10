from django.contrib import admin

# Register your models here.
from payment.models import Payment,Transaction

admin.site.register(Payment)
admin.site.register(Transaction)