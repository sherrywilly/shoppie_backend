from payment.models import  Payment,Transaction
from graphene import Node
from graphene_django import DjangoObjectType

class PaymentNode(DjangoObjectType):
    class Meta:
        model = Payment
        interfaces = (Node,)
