from django.contrib.sites.shortcuts import get_current_site
from graphene_django import DjangoObjectType
import graphene
from graphene import Node

from product.models import Product, ProductImage, ProductVideo


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (Node,)
        filter_fields = ('name', 'price',)
    desc = graphene.JSONString()
    pk = graphene.Int()
    def resolve_desc(self,info):
        x = self.desc
        # print(x)
        for i in x['blocks']:

            try:
                _x = i['data']['file']['url']
                i['data']['file']['url'] = info.context.build_absolute_uri(_x)
            except Exception as e:
                print(e)
        return x

    def resolve_pk(self, info):
        return self.pk


class ProductImageNode(DjangoObjectType):
    class Meta:
        model = ProductImage
        interfaces = (Node,)
        filter_fields = ('product_id',)

    pk = graphene.Int()
    image = graphene.String()

    def resolve_image(self, info):
        return info.context.build_absolute_uri(self.image.thumbnail['500x500'].url)

    def resolve_pk(self, info):
        return self.pk


class ProductVideoNode(DjangoObjectType):
    class Meta:
        model = ProductVideo
        # interfaces = (Node,)

    video = graphene.String()

    def resolve_video(self, info):
        return info.context.build_absolute_uri(self.video.url)

    pk = graphene.Int()

    def resolve_pk(self, info):
        return self.pk
