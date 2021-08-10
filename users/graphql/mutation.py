import base64
import graphene
import pyotp as pyotp
from django.contrib.auth import get_user_model
from graphql import GraphQLError
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token
from users.graphql.Type import UserType
from users.models import UserOtp
from users.utils import genKey


User = get_user_model()
class UserRegistrationMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String()
        email = graphene.String()
        password = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, self, info, phone, email, password):
        user = User.objects.create_user(phone, email, password)
        return UserRegistrationMutation(ok=True, user=user)


class SentOtpMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String()

    error = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, self, info, phone):
        try:
            if len(phone) == 10:
                __user = User.objects.get(phone=int(phone))
                key = base64.b32encode(genKey(__user.phone).encode())

                otp = pyotp.TOTP(key, interval=100)
                print(otp.now())
                __userotp, _ = UserOtp.objects.get_or_create(user_id=__user.id)
                __userotp.otp = otp.now()
                __userotp.save()
                print(otp.now())
                return SentOtpMutation(error=False, message="otp has been succesfully sented to you mobile number")

            else:
                raise GraphQLError("invalid phone number")
        except Exception as e:
            print(e)
            raise GraphQLError(e)


class VerifyOtpMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        otp = graphene.String(required=True)

    token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(UserType)

    # user = graphene.
    @classmethod
    def mutate(cls, self, info, phone, otp):
        __user = User.objects.get(phone=int(phone))
        key = base64.b32encode(genKey(__user.phone).encode())
        votp = pyotp.TOTP(key, interval=100)

        print(votp.now())
        if not votp.verify(str(__user.userotp.otp)):
            return GraphQLError("otp has been expired")

        if __user.userotp.otp == int(otp):
            print("otp verification is successfully")
            return VerifyOtpMutation(token=get_token(__user), refresh_token=create_refresh_token(__user), user=__user)
        else:
            print("failed to validate")
            raise GraphQLError("INVALID OTP")