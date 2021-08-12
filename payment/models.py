from django.db import models
import uuid
# Create your models here.
from django.db.models import F, Q, Sum

from order.models import Order


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('Created', "CREATED"),
        ('Authorized', "AUTHORIZED"),
        ('Captured', "CAPTURED"),
        ('Refunded', "REFUNDED"),
        ('PartiallyRefunded', 'PARTIALLY REFUNDED'),
        ('Failed', "FAILED")
    )
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    rzp_order_id = models.CharField(unique=True, max_length=100, blank=True, null=True,
                                    verbose_name="razorpay order id")
    signature = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(choices=PAYMENT_STATUS, default="Created", max_length=50)
    total = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    charged_value = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="payments")
    gateway_fee = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    raw_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    # def __str__(self):
    #     return self.rzp_order_id +" "+str(self.pk)

    @property
    def amount_refunded(self):
        _amount = self.transactions.filter(Q(type=2) | Q(type=3)).only('amount')
        x = [i.amount for i in _amount]
        return sum(x)

    @property
    def amount_valid_for_refund(self):
        x = self.amount_refunded
        return (self.total - x)


class Transaction(models.Model):
    TYPE_CHOICE = (
        (1, "PAYMENT"),
        (2, "REFUND"),
        (3, 'PARTIAL REFUND')
    )
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="transactions")
    type = models.IntegerField(choices=TYPE_CHOICE, default=1, blank=True)

    amount = models.DecimalField(decimal_places=2, max_digits=10)
    rzp_order_id = models.CharField(unique=True, max_length=100, blank=True, null=True,
                                    verbose_name="razorpay_order_id")

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, blank=True, null=True)
    method = models.CharField(max_length=100, blank=True, null=True)
    card_holder_name = models.CharField(verbose_name="Card Holder Name", max_length=100, blank=True, null=True)
    card_holder_network = models.CharField(verbose_name="card Holder Network", max_length=100, blank=True, null=True)
    card_issuer = models.CharField(verbose_name="card issuer", max_length=100, null=True, blank=True)
    card_last_4 = models.CharField(verbose_name="card last 4 digit numebers", max_length=100, blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    wallet = models.CharField(max_length=100, blank=True, null=True)
    vpa = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=12)
    fee = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    payment_token = models.CharField(null=True, blank=True, max_length=100)
    raw_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
