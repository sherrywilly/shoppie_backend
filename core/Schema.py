from graphene.types.schema import Schema
import  graphene

from cart.graphql.mutation import CartLineMutation
from order.graphql.mutation import AddressMutation, OrderMutation
from product.graphql.Query import Query as ProductQuery
class Query(ProductQuery,graphene.ObjectType):
    pass
class Mutation(graphene.ObjectType):
    add_to_cart = CartLineMutation.Field()
    add_address = AddressMutation.Field()
    checkout = OrderMutation.Field()

Schema = Schema(query=Query,mutation=Mutation)