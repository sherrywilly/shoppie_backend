import graphene

from payment.models import  Payment,Transaction
from graphene import Node
from graphene_django import DjangoObjectType

class PaymentNode(DjangoObjectType):
    class Meta:
        model = Payment
        # interfaces = (Node,)
    amount_refunded = graphene.Int()
    amount_valid_for_refund = graphene.Int()

    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk


    def resolve_amount_refunded(self,info):
        return  self.amount_refunded
    def resolve_amount_valid_for_refund(self,info):
        return  self.amount_valid_for_refund


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node ,)

    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk