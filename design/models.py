from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from order.models import Order, OrderLine


User = get_user_model()

class Design(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=100,verbose_name= "cart id")
    cart_line = models.CharField(max_length=100)
    image = models.ImageField(upload_to="order_image/",blank=False)
    video = models.FileField(upload_to="order_video/",blank=False)
    order_line = models.ForeignKey(OrderLine, on_delete=models.SET_NULL, blank=True, null=True)



    def __str__(self):
        return  self.cart_id