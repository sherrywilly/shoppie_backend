from utils.test_setup import TestSetup
from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from graphql_jwt.shortcuts import get_token

from cart.models import Cart, CartLine
from core.Schema import Schema
from graphene_django.utils.testing import GraphQLTestCase

# Create your tests here.
from order.models import Design

User = get_user_model()


class OrderTestCase(TestSetup, GraphQLTestCase):

    def setUp(self):
        self.create_test_user()

    def test_check_out_test_case_with_valid_details(self):
        """
        this test case the checks the checkout functionality with valid datas
        response = valid datas realated to payment and order details are expected
        have to check this request returning any error responses
        :return:
        """
        p1 = self.create_test_product()
        u = User.objects.get(phone="9744567054")

        token = get_token(u)

        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        cart, _ = Cart.objects.get_or_create(user=u)
        cartline = CartLine.objects.create(product_id=p1.pk, cart_id=cart.pk)
        Design.objects.create(cart_id=cart.pk, cart_line=cartline.pk, image=self.get_image(), video=self.get_image(),
                              user=u)
        self.assertTrue(self.client.login(
            phone="9744567054", password="anoop@123"))
        query = """
            mutation checkout($cartId: String!,$billingAddress:String!,$shippingAddress:String!){
              checkout(billingAddress:$billingAddress,shippingAddress:$shippingAddress,cartId:$cartId){
                payment{
                  rzpOrderId
                }
                order{
                  orderId
                  totalOrderValue
                }
              }
            }
        """
        x = self.query(query, variables={'billingAddress': self.create_test_address(user=u),
                                         'shippingAddress': self.create_test_address(user=u), 'cartId': str(cart.pk)})
        # print(x.json())
        self.assertResponseNoErrors(x)

    def test_check_out_test_case_with_invalid_datas(self):
        """
            this test case checks that the checking out with other users cart id

            response =  "make a request with valid datas"


            :param self:
            :return:
        """
        p1 = self.create_test_product()
        u = User.objects.get(phone="9744567054")
        cart, _ = Cart.objects.get_or_create(user=u)
        cartline = CartLine.objects.create(product_id=p1.pk, cart_id=cart.pk)
        Design.objects.create(cart_id=cart.pk, cart_line=cartline.pk, image=self.get_image(), video=self.get_image(),
                              user=u)
        self.create_test_user_two()
        self.assertTrue(self.client.login(
            phone="9544308787", password="anoop@123"))
        query = """
            mutation checkout($cartId: String!,$billingAddress:String!,$shippingAddress:String!){
              checkout(billingAddress:$billingAddress,shippingAddress:$shippingAddress,cartId:$cartId){
                payment{
                  rzpOrderId
                }
                order{
                  orderId
                  totalOrderValue
                }
              }
            }
        """
        x = self.query(query, variables={'billingAddress': self.create_test_address(user=u),
                                         'shippingAddress': self.create_test_address(user=u), 'cartId': str(cart.pk)})
        # print(x.json())
        self.assertResponseHasErrors(x)

    def test_get_my_orders(self):
      query = """
     query{
            myOrders{
              edges{
                node{
                  orderId
                
                  totalOrderValue
                }
              }
            }
          }
      """
      self.client.login(phone="9744567054", password="anoop@123")
      x = self.query(query)
      self.assertResponseNoErrors(x)
