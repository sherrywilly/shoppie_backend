from django.contrib.auth import get_user_model
from django.db import models
import uuid
from product.models import Product

User = get_user_model()


# Create your models here.

class Address(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_one = models.TextField()
    address_two = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=10)
    area = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Order(models.Model):
    ORDER_STATUS = (('Pending', 'Pending'), ('processing', 'Processing'), ('packed', 'Packed'),
                    ('shipped', 'Shipped'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'),
                    ('returned', 'Returned'), ('cancelled', 'Cancelled'))
    order_id = models.CharField(max_length=100, default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name="billing_address")
    shipping_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name="shipping_address")
    total_order_value = models.DecimalField(decimal_places=2, max_digits=6,blank=True,null=True)
    shipping_charges = models.DecimalField(default=00, decimal_places=2, max_digits=6)
    cart_id = models.CharField(blank=True, max_length=100)
    is_payment_successfull = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def basic_amount(self):
        try:
            x = sum(i.price for i in self.orderitems.all())
        except:
            x = 0
        return x

    @property
    def shipping_charge(self):
        base = self.basic_amount
        return (0 if base >= 500 else 80)

    def __str__(self):
        return str(self.order_id)


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def price(self):
        return self.product.price


class Design(models.Model):
    order_line = models.ForeignKey(OrderLine, on_delete=models.PROTECT, null=True, related_name="design")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=100, verbose_name="cart id", blank=True, null=True)
    cart_line = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="order_image/", blank=False)
    video = models.FileField(upload_to="order_video/", blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.cart_id
