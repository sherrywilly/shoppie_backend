from django.contrib.auth import get_user_model
from graphene import Node
from graphene_django import DjangoObjectType

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
        fields = ('phone','email','is_superuser','is_user','is_active')