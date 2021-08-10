from django.db import models
import  uuid
# Create your models here.
from order.models import Order



class Payment(models.Model):
    PAYMENT_STATUS = (
        ('Created',"CREATED"),
        ('Authorized',"AUTHORIZED"),
        ('Captured',"CAPTURED"),
        ('Refunded',"REFUNDED"),
        ('Failed',"FAILED"),

    )
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)

    rzp_order_id = models.CharField(unique=True,max_length=100,blank=True,null=True,verbose_name="razorpay_order_id")
    signature = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(choices=PAYMENT_STATUS,default="Created",max_length=50)
    total =  models.DecimalField(decimal_places=2, max_digits=6)
    charged_value =  models.DecimalField(decimal_places=2, max_digits=6)
    order = models.ForeignKey(Order,on_delete=models.DO_NOTHING,blank=True,null=True)
    gateway_fee =  models.DecimalField(decimal_places=2, max_digits=6,default=0)
    raw_data = models.JSONField(blank=True,null=True)

class Transaction(models.Model):
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    ##########  ----> TYPE
    # type = models.

    amount =  models.DecimalField(decimal_places=2, max_digits=6)
    rzp_order_id = models.CharField(unique=True, max_length=100, blank=True, null=True,
                                    verbose_name="razorpay_order_id")

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, blank=True, null=True)
    method = models.CharField(max_length=100,blank=True,null=True)
    card_holder_name = models.CharField(verbose_name="Card Holder Name",max_length=100,blank=True,null=True)
    card_holder_network = models.CharField(verbose_name="card Holder Network",max_length=100,blank=True,null=True)
    card_issuer = models.CharField(verbose_name="card issuer",max_length=100,null=True,blank=True)
    card_last_4 = models.CharField(verbose_name="card last 4 digit numebers",max_length=100,blank=True,null=True)
    bank = models.CharField(max_length=100,blank=True,null=True)
    wallet = models.CharField(max_length=100,blank=True,null=True)
    vpa = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(blank=True,null=True,max_length=12)
    fee = models.DecimalField(decimal_places=2,max_digits=6,default=0)
    payment_token = models.CharField(null=True,blank=True,max_length=100)
    raw_data = models.JSONField(blank=True,null=True)
