from django.core.checks import messages
from order.graphql.type import OrderLineNode
from django.contrib.auth import get_user_model
import graphene
from graphql import GraphQLError, error
from graphql_jwt.decorators import login_required

from cart.graphql.type import CartLineNode, CartNode
from cart.models import Cart, CartLine
from order.models import Design

from product.models import Product
from django.db import transaction

User = get_user_model()


class CartLineMutation(graphene.Mutation):
    class Arguments:
        product = graphene.Int(required=True)
    cart = graphene.Field(CartNode)

    @classmethod
    @login_required
    def mutate(cls, self, info, product, **kwargs):
        # print(info.context.user)
        user_id = info.context.user.pk
        # user_id = User.objects.get(phone="9744567054").pk
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        try:
            with transaction.atomic():
                try:
                    _product = Product.objects.get(id=product)
                except:
                    raise GraphQLError("Invalid product id")
                _cartlilne = CartLine.objects.create(
                    cart=cart, product=_product, price=_product.price)
                _design = Design()
                try:
                    _design.cart_id = cart.pk
                    _design.cart_line = _cartlilne.pk
                    _design.user_id = user_id
                    _design.image = info.context.FILES['cart_img']
                    _design.video = info.context.FILES['cart_video']
                    _design.save()
                except Exception as e:
                    raise GraphQLError(
                        f"please attach the  image and video to add this product {info.context.FILES}")
            return CartLineMutation(cart=cart)
        except Exception as e:
            raise GraphQLError(e)


class CartLineDeletionMutation(graphene.Mutation):
    class Arguments:
        cart_id = graphene.String(required=True)
        cart_item_id = graphene.String(required=True)
    status = graphene.String()
    message = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, cart_id, cart_item_id):
        try:
            cart = Cart.objects.get(id=cart_id, user_id=info.context.user.pk)
        except:
            raise GraphQLError("invalid cart id")
        try:
            cart_item = cart.cart_items.get(id=cart_item_id)
            print(cart_item)
        except:
            raise GraphQLError('invalid cart item')
        cart_item.delete()
        return CartLineDeletionMutation(status="ok",message="successfully deleted the cart item")
