from django.db import models
from django.contrib.auth import get_user_model
import uuid
import  razorpay


from product.models import Product

User = get_user_model()


# Create your models here.
class Cart(models.Model):
    id = models.UUIDField(max_length=100, default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def basic_price(self):
        try:
            x = sum((i.product.price for i in self.cart_items.all()))
        except Exception as e:
            x = 0
        return x





class CartLine(models.Model):
    id = models.UUIDField(max_length=100, default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=00, decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.product.name
