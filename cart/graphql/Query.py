from graphene_django.filter import DjangoFilterConnectionField
import graphene

from cart.graphql.type import CartNode
from cart.models import Cart


class Query(graphene.ObjectType):
    my_cart = DjangoFilterConnectionField(CartNode)


    def resolve_my_cart(self,info):
        user = info.context.user
        cart,_ = Cart.objects.get_or_create(user=user)
        return cart