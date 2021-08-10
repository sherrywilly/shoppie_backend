from  graphene_django import  DjangoObjectType
import graphene
from graphene import  Node

from product.models import Product, ProductImage, ProductVideo


class ProductNode(DjangoObjectType):
    class Meta:
        model= Product
        interfaces = (Node,)
        filter_fields = ('name','price',)

    pk = graphene.Int()

    def resolve_pk(self, info):
        return self.pk


class ProductImageNode(DjangoObjectType):
    class Meta:
        model = ProductImage
        interfaces = (Node,)
        filter_fields = ('product_id',)

    pk = graphene.Int()

    def resolve_pk(self, info):
        return self.pk

class ProductVideoNode(DjangoObjectType):
    class Meta:
        model = ProductVideo
        # interfaces = (Node,)


    pk = graphene.Int()

    def resolve_pk(self, info):
        return self.pk
