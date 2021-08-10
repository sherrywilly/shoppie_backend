import uuid

from django.db import models

# Create your models here.
from versatileimagefield.fields import VersatileImageField, PPOIField


class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=10)
    tax_rate = models.CharField(max_length=128, blank=True, null=True, default=0)
    weight = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    price = models.DecimalField(default=00,decimal_places=2, max_digits=6)

    class Meta:
        # app_label = "products"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_first_image(self):
        images = list(self.images.all())
        return images[0] if images else self.product.get_first_image()

    def get_featured_image(self):
        image = self.images.filter(is_featured=True).first()
        return image

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,related_name="images"
    )
    image = VersatileImageField(upload_to="products", ppoi_field="ppoi", blank=False)
    ppoi = PPOIField()
    is_featured = models.BooleanField(default=False)
    alt = models.CharField(max_length=128, blank=True)




    def get_ordering_queryset(self):
        return self.product.images.all()

    def save(self, *args, **kwargs):
        img_name = self.image.name[:len(self.product.name)]
        if not len(img_name) > 50:
            self.image.name = str(uuid.uuid4()) + " - " + self.image.name
        super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name + " - " + self.image.name



class ProductVideo(models.Model):
    product = models.ForeignKey(
        Product, related_name="video", on_delete=models.CASCADE
    )
    video = models.FileField(upload_to='products/videos',blank=False)


    def save(self, *args, **kwargs):
        vid_name = self.video.name[:len(self.product.name)]
        if not len(vid_name) > 50:
            self.video.name = str(uuid.uuid4()) + " - " + self.video.name
        super(ProductVideo, self).save(*args, **kwargs)