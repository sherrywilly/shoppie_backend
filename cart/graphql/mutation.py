import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from cart.graphql.type import CartNode
from cart.models import Cart, CartLine
from order.models import Design

from product.models import Product
from django.db import transaction


class CartLineMutation(graphene.Mutation):
    class Arguments:
        cart_id = graphene.ID()

        product = graphene.Int(required=True)
        price = graphene.Int(required=True)

    cart = graphene.Field(CartNode)

    @classmethod
    @login_required
    def mutate(cls, self, info, product, price, **kwargs):
        # user = info.context.user ||0
        # print(kwargs.get())
        user_id = 1
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        try:
            with transaction.atomic():
                _product = Product.objects.get(id=product)
                _cartlilne = CartLine.objects.create(cart=cart, product=_product, price=price)
                _design = Design()
                try:
                    _design.cart_id = cart.pk
                    _design.cart_line = _cartlilne.pk
                    _design.user_id = user_id
                    _design.image = info.context.FILES['cart_img']
                    _design.video = info.context.FILES['cart_video']
                    _design.save()
                except:
                    raise GraphQLError("please attach the  image and video to add this product")
            return CartLineMutation(cart=cart)
        except Exception as e:
            raise GraphQLError(e)
