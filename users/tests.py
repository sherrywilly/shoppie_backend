from re import S
from django.contrib.auth import get_user_model
from django.db.models import query
from django.test import TestCase
from utils.test_setup import TestSetup
from graphene_django.utils.testing import GraphQLTestCase

# Create your tests here.


class UserRegistrationTestCase(TestSetup, GraphQLTestCase):

    def sent_registration(self, phone, email, password):
        query = """
       mutation registerUser($phone :String!,$email:String!,$password:String!){
         registerUser(phone:$phone,email:$email,password:$password){
             ok
            message
            }
            }
        """
        res = self.query(query, variables={
                         'phone': phone, 'email': email, 'password': password})
        return res.json()

    def test_registration_with_invalid_phone(self):
        '''
        it will verify that the phone no shoulkd be 10 numbers         
        '''
        res = self.sent_registration(
            "88687687", "sherry@gmail.com", 'Athul@123')

        assert res['errors'][0]['message'] == "Mobile no should be 10 numbers"

    def test_registration_with_invalid_email(self):
        '''
        it will verify that a  valid email can enter into our network
        '''
        res = self.sent_registration(
            "9544308787", "sherrygmail.com", 'Athul@123')
        assert res['errors'][0]['message'] == "please provide a valid email"

    def test_registration_with_invalid_password_having_less_than_eight_char(self):
        '''
        a valid password should have min 8 charaters and not to be only numbers
        '''
        res = self.sent_registration("9744567054", "sherry@gmail.com", 'A123')
        print(res)
        assert res['errors'][0]['message'] == "['This password is too short. It must contain at least 8 characters.']"

    def test_registration_with_invalid_password_with_only_numerics(self):
        '''

        a valid password should have min 8 charaters and not to be only numbers and it should be stroog passwords can be used

        '''
        res = self.sent_registration(
            "9744567054", "sherry@gmail.com", '12365757567')
        assert res['errors'][0]['message'] == "['This password is entirely numeric.']"

    def test_registration_With_valid_datas(self):
        '''
        this will test the registration with valid datas
        '''
        res = self.sent_registration(
            "9744567054", "sherry@gmail.com", 'Athul@1376')
        self.assertTrue(res['data']['registerUser']['ok'])


    #!############################# user registration Test ended ###############################
User = get_user_model()

    #!############################# user Login and Otp Verification starts ##############################
class UserLoginTestCase(TestSetup, GraphQLTestCase):
    def setUp(self):
        self.create_test_user()
        return super().setUp()

    def sent_login(self, phone):
        query = """
        mutation login($phone:String!){
              login(phone:$phone){
                error
                message
              }
            }
        """
        res = self.query(
            query, variables={'phone': phone}
        )
        return res.json()

    def test_sent_otp_with_unregistered_phone_number(self):
        res = self.sent_login(phone="76876877887")
        print("---------------------+++++++++++++++-------------------------")
        self.assertEqual(res['errors'][0]['message'], 'invalid phone number')

    def test_sent_otp_with_registered_phone_number(self):
        res = self.sent_login(phone="9744567054")
        print("---------------------+++++++++++++++-------------------------")
        print(res)
        self.assertFalse(res['data']['login']['error'])
        self.assertEqual(res['data']['login']['message'],
                         'otp has been succesfully sented to you mobile number')

    def verify_otp(self, phone, otp):
        query = """
        mutation verifylogin($phone:String!,$otp:String!){
            verifyLogin(phone:$phone,otp:$otp){
              token
              refreshToken
              user{
                phone
              }
            }
            }
        """
        res = self.query(query, variables={
            'phone': phone, 'otp': otp
        })
        return res.json()

    def test_verify_otp_with_invalid_number(self):
        res =self.verify_otp('9846545645','464564')
        self.assertEqual(res['errors'][0]['message'],'Invalid request with unregistered phone number')

    def test_verify_otp_with_valid_details(self):
        phone = '9744567054'
        self.sent_login(phone)
        user = User.objects.get(phone=phone)
        res = self.verify_otp(phone,otp=user.userotp.otp)
        print(res)
        self.assertEqual(res['data']['verifyLogin']['user']['phone'],phone)

    def test_verify_otp_with_invalid_otp(self):
        phone = '9744567054'
        self.sent_login(phone)
        res = self.verify_otp(phone,"658767")
        self.assertEqual(res['errors'][0]['message'],'INVALID OTP')