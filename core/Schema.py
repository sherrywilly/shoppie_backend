from graphene.types.schema import Schema
import graphene

from cart.graphql.mutation import CartLineMutation
from order.graphql.mutation import AddressMutation, OrderMutation
from product.graphql.Query import Query as ProductQuery
from order.graphql.Query import Query as OrderQuery
from users.graphql.mutation import VerifyOtpMutation, SentOtpMutation, UserRegistrationMutation


class Query(ProductQuery, OrderQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    add_to_cart = CartLineMutation.Field()
    add_address = AddressMutation.Field()
    checkout = OrderMutation.Field()
    login = SentOtpMutation.Field()
    verify_login = VerifyOtpMutation.Field()
    registerUser = UserRegistrationMutation.Field()


Schema = Schema(query=Query, mutation=Mutation)
