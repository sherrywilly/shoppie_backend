import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField

from product.graphql.Type import  ProductNode

class Query(graphene.ObjectType):
    all_product = DjangoFilterConnectionField(ProductNode)