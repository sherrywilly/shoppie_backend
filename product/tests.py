import json
from graphene_django.utils.testing import GraphQLTestCase

from product.models import Product

import tempfile

from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token

from product.models import Product

User = get_user_model()


class ProductTestCase(GraphQLTestCase):

    def setUp(self):
        User.objects.create_user(email="test@gmail.com", phone="9744567054", password="dsfSdfdsf@123213")

        p = Product()
        p.name = "Test"
        p.price = "1000"
        p.desc = {}
        p.height = 0
        p.width = 0
        p.weight = 0
        p.length = 0
        p.save()

    def test_product_query(self):
        print("++++++++++++++++++++++++++ test product query ++++++++++++++++++++++++")
        response = self.query(
            '''
            query{
   allProduct{
    edges{
      node{
        id
        pk
        name
        taxRate
        price
        createdAt
      }
    }
  }
}
            '''

        )
        content = json.loads(response.content)
        print(content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)



# def create_product():