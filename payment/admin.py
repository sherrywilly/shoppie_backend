from django.contrib import admin

# Register your models here.
from payment.models import Payment,Transaction

# admin.site.register(Payment)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('amount_refunded','id','amount_valid_for_refund','total')
admin.site.register(Transaction)