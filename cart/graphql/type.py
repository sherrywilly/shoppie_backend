import graphene
from graphene_django import DjangoObjectType
from graphene import Node
from cart.models import Cart, CartLine


class CartNode(DjangoObjectType):
    class Meta:
        model = Cart
        filter_fields = ('created_by', 'id')
        interfaces = (Node,)

    pk = graphene.String()
    basic_price = graphene.String()

    def resolve_basic_price(self, info):
        return self.basic_price

    def resolve_pk(self, info):
        return self.pk


class CartLineNode(DjangoObjectType):
    class Meta:
        model = CartLine
        interfaces = (Node,)

    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk
