from graphene_django import  DjangoObjectType
from graphene import Node
from order.models import Address, Order,OrderLine


class Addressnode(DjangoObjectType):
    class Meta:
        model= Address
        interfaces = (Node,)
        # filter_fields = ['user',]



class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (Node,)

class OrderLineNode(DjangoObjectType):
    class Meta:
        model  = OrderLine
        interfaces = (Node,)

