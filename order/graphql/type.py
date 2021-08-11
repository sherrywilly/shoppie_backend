import graphene
from graphene_django import DjangoObjectType
from graphene import Node
from order.models import Address, Order, OrderLine, Design


class Addressnode(DjangoObjectType):
    class Meta:
        model = Address
        interfaces = (Node,)
        # filter_fields = ['user',]

    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (Node,)
        filter_fields = ('user', 'order_id')

    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk
    # @classmethod
    # def get_node(cls, info, id):
    #     try:
    #         order = cls._meta.model.objects.get(id=id)
    #     except cls._meta.model.DoesNotExist:
    #         return None
    #
    #     if info.context.user == order.user:
    #         return order
    #     return None


class OrderLineNode(DjangoObjectType):
    class Meta:
        model = OrderLine
        interfaces = (Node,)

    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk


class DesignNode(DjangoObjectType):
    class Meta:
        model = Design
        interface = (Node,)
        # fields = ('design',)

    image = graphene.String()
    video = graphene.String()

    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk

    def resolve_video(self, info):
        return info.context.build_absolute_uri(self.video.url)

    def resolve_image(self, info):
        return info.context.build_absolute_uri(self.image.url)
