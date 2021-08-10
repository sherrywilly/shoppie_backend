from django.contrib import admin
from product.models import Product,ProductVideo,ProductImage
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVideo)