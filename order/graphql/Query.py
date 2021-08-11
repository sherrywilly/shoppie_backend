import graphene
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from order.graphql.type import OrderNode
from order.models import Order




class Query(graphene.ObjectType):
    my_orders = DjangoFilterConnectionField(OrderNode)
    get_order_by_id = graphene.Field(OrderNode,id=graphene.String())

    @login_required
    def resolve_get_order_by_id(self,info,id):
        try:
            _order = Order.objects.get(order_id=id)
        except Exception as e:
            raise GraphQLError("invalid order id! please provide valid information")
        if _order.user == info.context.user:
            return _order
        else:
            raise GraphQLError("invalid user")
    @login_required
    def resolve_my_orders(self,info):
        user = info.context.user
        print(user)
        return Order.objects.filter(user=user)