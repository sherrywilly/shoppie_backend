import graphene
import razorpay
from graphql import GraphQLError
from cart.models import Cart
from core.settings import RAZORPAY_KEY, RAZORPAY_SECRET
from design.models import Design
from order.graphql.type import Addressnode, OrderNode
from order.models import Address, Order,OrderLine
from django.db import transaction
from payment.graphql.type import PaymentNode
from payment.models import Transaction as Trans,Payment
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
    def mutate(cls,self,info,first_name,last_name,address_one,mobile,area,pincode,state,id=None,**kwargs):
        user_id = 1
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
        return  AddressMutation(address = address)

class OrderMutation(graphene.Mutation):
    class Arguments:
        # billing and Shipping address are foregn keys
        billing_address = graphene.String(required=True)
        shipping_address = graphene.String(required=True)
        cart_id = graphene.String(required=True)

    order = graphene.Field(OrderNode)
    payment = graphene.Field(PaymentNode)
    @classmethod
    def mutate(cls,self,info,billing_address,shipping_address,cart_id):
        __cart = Cart.objects.get(pk = cart_id)
        user_id  = 1
        try:
            with transaction.atomic():
                order = Order()
                order.billing_address_id = int(billing_address)
                order.shipping_address_id= int(shipping_address)
                order.cart_id = __cart.pk
                order.user_id =user_id
                order.total_order_value = __cart.basic_price
                order.save()
                for i  in __cart.cart_items.all():
                    __orderline= OrderLine.objects.create(product=i.product,order=order)
                    _temp = Design.object.get(cartline=__cart.pk)
                    _temp.order_line_id = __orderline.pk
                __cart.delete()

                pay_order = client.order.create(
                    {'amount': int(order.basic_amount) * 100, 'currency': "INR", 'receipt': str(order.pk), 'payment_capture': 1})
                payment = Payment()

                payment.rzp_order_id = pay_order.get('id')
                payment.total = order.basic_amount
                payment.charged_value = order.basic_amount
                payment.raw_data = pay_order
                payment.save()
            return  OrderMutation(order= order,)
        except Exception as e:
            print(e)
            raise GraphQLError(e)









