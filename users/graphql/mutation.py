import base64
import graphene
import pyotp as pyotp
from django.contrib.auth import get_user_model
from django.db.models import F
from graphql import GraphQLError
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token
from users.graphql.Type import UserType
from users.models import UserOtp
from users.utils import genKey
import re
from django.contrib.auth.password_validation import validate_password
User = get_user_model()


EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
# PASSWORD_REGEX = r"/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&.])[A-Za-z\d$@$!%*?&.]{6, 20}/"
ONLY_NUM_REGEX = r"^[0-9]*$"
class UserRegistrationMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String()
        email = graphene.String()
        password = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(UserType)
    message = graphene.String()

    @classmethod
    def mutate(cls, self, info, phone, email, password):
        if len(phone) !=10 and re.match(ONLY_NUM_REGEX,phone):
            raise GraphQLError("Mobile no should be 10 numbers") 
        elif email and not re.match(EMAIL_REGEX,email):
            raise GraphQLError("please provide a valid email")
        validate_password(password=password)

        try:
            user = User.objects.create_user(phone, email, password)
            return UserRegistrationMutation(ok=True, user=user,
                                            message="you are successfully registered with our system")
        except Exception as e:
            raise GraphQLError(e)


# class Myprofile(graphene.Mutation):
#     class Arguments:
#         id = graphene.String()
#
#     user = graphene.Field(UserType)
#
#     def mutate(cls, self, info, id=None):
#         return Myprofile()


class SentOtpMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String()

    error = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, self, info, phone):
        try:
            if len(phone) == 10:
                try:
                    __user = User.objects.get(phone=int(phone))
                except:
                    raise GraphQLError("This number is not present in our system")

                key = base64.b32encode(genKey(__user.phone).encode())

                otp = pyotp.TOTP(key, interval=1000)
                print(otp.now())
                __userotp, _ = UserOtp.objects.get_or_create(user=__user)
                # if __userotp.counter >= 15:
                #     raise GraphQLError("You have reached the otp limit")
                __userotp.otp = otp.now()
                # __userotp.counter = F('counter') + 1
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
        try:
            __user = User.objects.get(phone=int(phone))
        except:
            raise GraphQLError("Invalid request with unregistered phone number")
        key = base64.b32encode(genKey(__user.phone).encode())
        votp = pyotp.TOTP(key, interval=1000)

        print(votp.now())
        if not votp.verify(str(__user.userotp.otp)):
            return GraphQLError("otp has been expired")

        if __user.userotp.otp == int(otp):
            __user.userotp.counter = 0
            __user.userotp.save()
            print("otp verification is successfully")
            return VerifyOtpMutation(token=get_token(__user), refresh_token=str(create_refresh_token(__user)),
                                     user=__user)
        else:
            print("failed to validate")
            raise GraphQLError("INVALID OTP")
