from uuid import uuid4
from utils.test_setup import TestSetup
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model, login
from graphql_jwt.shortcuts import get_token
from graphene.test import Client
from django.urls import reverse
from core.Schema import Schema
from product.models import Product
from io import BytesIO
from PIL import Image
from uuid import uuid4
User = get_user_model()


def get_image(name='test.png', ext='png', size=(1, 1), color=(0, 0, 0)):
    file_obj = BytesIO()
    image = Image.new('RGBA', size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return SimpleUploadedFile(name, file_obj.getvalue(), content_type='image/png')


class TestProductcart(TestCase):
    def setUp(self):
        User.objects.create_user(
            email="test@gmail.com", phone="9744567054", password="dsfSdfdsf@123213")
        p = Product()
        p.name = "Test"
        p.price = "1000"
        p.desc = {}
        p.height = 0
        p.width = 0
        p.weight = 0
        p.length = 0
        p.save()
        print("product_id")
        print(p.pk)
        # return super().setUp()

    def test_product_cart_adding_With_valid(self):
        payload = '''mutation{
      addToCart(product:7){
        cart{
          id
          user{
                  id
                }
                cartItems{
                  edges{
                    node{
                      id
                      product{
                        id
                      }
                    }
                  }
                }
              }
            }
          }
                '''

        path = reverse('graph')
        token = get_token(User.objects.get(phone="9744567054"))
        print(token)
        self.assertTrue(self.client.login(
            phone="9744567054", password="dsfSdfdsf@123213"),)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        x = self.client.post(path=path, data={'query': payload, 'cart_img': get_image(),
                                              'cart_video': get_image()}, format="multipart", headers=headers)
        data = x.json()
        self.assertTrue(data['data']['addToCart']['cart'])

    def test_product_cart_adding_With_invalid_data(self):
        payload = '''mutation{
      addToCart(product:20){
        cart{
          id
          user{
                  id
                }
                cartItems{
                  edges{
                    node{
                      id
                      product{
                        id
                      }
                    }
                  }
                }
              }
            }
          }
                '''

        path = reverse('graph')
        self.assertTrue(self.client.login(
            phone="9744567054", password="dsfSdfdsf@123213"), )

        x = self.client.post(path=path, data={'query': payload, 'cart_img': get_image(),
                                              'cart_video': get_image()}, format="multipart")

        data = x.json()
        self.assertEqual(data['errors'][0]['message'], 'Invalid product id')

        # print(x)


class CartItemDeletionTestCase(TestSetup, GraphQLTestCase):
    def setUp(self):
        self.create_test_product()
        self.create_test_user()

    def sent_delete_request(self, cart_id, cart_item_id):
        self.client.login(phone="9744567054", password="anoop@123")
        query = """
      mutation dropCartItem($cartId:String!,$cartItemId:String!){
          dropCartItem(cartId:$cartId,cartItemId:$cartItemId){
            status
            message
          }
        }
      
      """
        res = self.query(query, variables={
                         'cartId': cart_id, 'cartItemId': cart_item_id})
        return res.json()

    def test_cart_item_deletion_with_valid_data(self):
        cart = self.create_test_cart()
        cart_item = cart.cart_items.all()[0]

        x = self.sent_delete_request(cart_id=str(
            cart.pk), cart_item_id=str(cart_item.pk))

        self.assertEqual(x['data']['dropCartItem']['status'], 'ok')
        self.assertEqual(x['data']['dropCartItem']['message'],
                         'successfully deleted the cart item')
    

    def test_cart_item_deletion_with_invalid_cart_item_id(self):
        cart = self.create_test_cart()
        cart_item = cart.cart_items.all()[0]
        x = self.sent_delete_request(cart_id=str(
            cart.pk), cart_item_id=str(uuid4()))
        self.assertEqual(x['errors'][0]['message'],"invalid cart item")

    def test_cart_item_deletion_with_invalid_cart_item_id(self):
    
        x = self.sent_delete_request(cart_id=str(
            uuid4()), cart_item_id=str(uuid4()))
        # print(x)
        self.assertEqual(x['errors'][0]['message'],'invalid cart id')

    def test_get_my_cart(self):
      cart = self.create_test_cart()
      query = """
      query{
           myCart{
            id
            cartItems{
              edges{
                node{
                  id
                }
              }
            }
          }
          }
      """
      self.client.login(phone="9744567054", password="anoop@123")
      x = self.query(query)
      self.assertResponseNoErrors(x)