import graphene
import razorpay
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from cart.models import Cart
from core.settings import RAZORPAY_KEY, RAZORPAY_SECRET

from order.graphql.type import Addressnode, OrderNode
from order.models import Address, Order, OrderLine, Design
from django.db import transaction
from payment.graphql.type import PaymentNode
from payment.models import Transaction as Trans, Payment

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))


class AddressMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        address_one = graphene.String(required=True)
        address_two = graphene.String()
        company_name = graphene.String()
        mobile = graphene.String(required=True)
        area = graphene.String(required=True)
        pincode = graphene.String(required=True)
        state = graphene.String(required=True)
        id = graphene.String()

    address = graphene.Field(Addressnode)

    @classmethod
    @login_required
    def mutate(cls, self, info, first_name, last_name, address_one, mobile, area, pincode, state, id=None, **kwargs):
        user_id = info.context.user.id
        try:
            if id is not None:
                address = Address.objects.get(id=id)
            else:
                address = Address()
            address.first_name = first_name
            address.last_name = last_name
            address.address_one = address_one
            address.address_two = kwargs.get('address_two', None)
            address.company_name = kwargs.get('company_name', None)
            address.mobile = mobile
            address.area = area
            address.pincode = pincode
            address.state = state
            address.created_by_id = user_id
            address.save()

        except Exception as e:
            print(e)
            raise GraphQLError(e)
        return AddressMutation(address=address)


class OrderMutation(graphene.Mutation):
    class Arguments:
        # billing and Shipping address are foreign keys
        billing_address = graphene.String(required=True)
        shipping_address = graphene.String(required=True)
        cart_id = graphene.String(required=True)

    order = graphene.Field(OrderNode)
    payment = graphene.Field(PaymentNode)

    @classmethod
    @login_required
    def mutate(cls, self, info, billing_address, shipping_address, cart_id):
        user_id = info.context.user.pk
        try:
            __cart = Cart.objects.get(pk = cart_id,user_id = user_id)
        except Exception as e:
            raise GraphQLError("please make request with valid data")


        try:
            with transaction.atomic():
                order = Order()
                order.billing_address_id = int(billing_address)
                order.shipping_address_id = int(shipping_address)
                order.cart_id = __cart.pk
                order.user_id = user_id
                order.total_order_value = __cart.basic_price
                order.save()
                cart_items = __cart.cart_items.all()
                if cart_items.count() == 0:
                    raise GraphQLError("this cart did not have any items")
                for i in cart_items:
                    __orderline = OrderLine.objects.create(product=i.product, order=order)
                    _temp = Design.objects.get(cart_line=i.pk)
                    _temp.order_line_id = __orderline.pk
                    _temp.save()
                __cart.delete()
                pay_order = client.order.create(
                    {'amount': int(order.basic_amount) * 100, 'currency': "INR", 'receipt': str(order.pk),
                     'payment_capture': 1})
                payment, _ = Payment.objects.get_or_create(rzp_order_id=pay_order.get('id'))
                print(order.basic_amount)
                payment.total = order.total_order_value
                payment.order = order
                # payment.charged_value = order.total_order_value
                payment.raw_data = pay_order
                payment.save()
            return OrderMutation(order=order, payment=payment)
        except Exception as e:
            print(e)
            raise GraphQLError(e)
