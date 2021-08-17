from graphene_django.filter import DjangoFilterConnectionField
import graphene
from graphql_jwt.decorators import login_required

from cart.graphql.type import CartNode
from cart.models import Cart


class Query(graphene.ObjectType):
    my_cart = graphene.Field(CartNode)

    @login_required
    def resolve_my_cart(self, info):
        user = info.context.user
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart
