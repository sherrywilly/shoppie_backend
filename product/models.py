import uuid

from django.db import models

# Create your models here.
from django_editorjs_fields import EditorJsJSONField
from versatileimagefield.fields import VersatileImageField, PPOIField


class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = EditorJsJSONField(
        plugins=[
            "@editorjs/image",
            "@editorjs/header",
            "@editorjs/list",
            "editorjs-github-gist-plugin",
            "editorjs-hyperlink",
            "@editorjs/code",
            "@editorjs/inline-code",
            "@editorjs/table@1.3.0",
        ],
        tools={
            "Gist": {
                "class": "Gist"
            },
            "Hyperlink": {
                "class": "Hyperlink",
                "config": {
                    "shortcut": 'CMD+L',
                    "target": '_blank',
                    "rel": 'nofollow',
                    "availableTargets": ['_blank', '_self'],
                    "availableRels": ['author', 'noreferrer'],
                    "validate": False,
                }
            },
            # "Image": {
            #     'class': 'ImageTool',
            #     "config": {
            #         "endpoints": {
            #             # Your custom backend file uploader endpoint
            #             "byFile": "/editorjs/image_upload/"
            #         }
            #     }
            # }
        },
        null=True,
        blank=True,
    )
    tax_rate = models.CharField(max_length=128, blank=True, null=True, default=0)
    weight = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    price = models.DecimalField(default=00, decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

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
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = VersatileImageField(upload_to="products", ppoi_field="ppoi", blank=False)
    ppoi = PPOIField()
    is_featured = models.BooleanField(default=False)
    alt = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

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
    video = models.FileField(upload_to='products/videos', blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        vid_name = self.video.name[:len(self.product.name)]
        if not len(vid_name) > 50:
            self.video.name = str(uuid.uuid4()) + " - " + self.video.name
        super(ProductVideo, self).save(*args, **kwargs)
