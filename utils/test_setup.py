from cart.models import Cart, CartLine
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import  TestCase
from faker import Faker
from django.contrib.auth import  get_user_model
from io import BytesIO

from order.models import Address, Design, Order, OrderLine
from product.models import Product

User = get_user_model()
class TestSetup(TestCase):

    def get_image(self,name='test.png', ext='png', size=(1, 1), color=(0, 0, 0)):
        file_obj = BytesIO()
        image = Image.new('RGBA', size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return SimpleUploadedFile(name, file_obj.getvalue(), content_type='image/png')

    def create_test_user(self):
        user =User.objects.create_user(phone = "9744567054",email="tesuser@gamil.com",password="anoop@123")
        return user

    def create_test_user_two(self): 
        user =User.objects.create_user(phone = "9544308787",email="tesusertwo@gamil.com",password="anoop@123")
        return user

    def create_test_product(self):
        p = Product()
        p.name = "Test"
        p.price = "1000"
        p.desc = {}
        p.height = 0.00
        p.width = 0
        p.weight = 0
        p.length = 0
        p.save()
        return  p

    def create_test_address(self,user):
        faker = Faker()
        address = Address()
        address.first_name = faker.first_name()
        address.last_name = faker.last_name()
        address.address_one = faker.address()
        address.address_two = faker.address()
        address.mobile = faker.phone_number()[:10]
        address.area = "chennai"
        address.state = "Tamil Nadu"
        address.pincode = "600203"
        address.created_by = user
        address.save()
        return  str(address.pk)

    def create_test_cart(self):
        p1=self.create_test_product()
        u = User.objects.get(phone="9744567054")
        cart, _ = Cart.objects.get_or_create(user=u)
        cartline = CartLine.objects.create(product_id=p1.pk, cart_id=cart.pk)
        Design.objects.create(cart_id=cart.pk, cart_line=cartline.pk, image=self.get_image(), video=self.get_image(),
                              user=u)
        return cart





