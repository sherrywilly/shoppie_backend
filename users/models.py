from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, phone, password, **kwargs):

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_user', False)

        if kwargs.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(phone, password, **kwargs)

    def create_user(self, phone,email, password, **kwargs):
        user = self.model(phone=phone,email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,10}$',
        message="Phone must be in the format: '+999999999'.Please enter 10 digits mobile number.")
    phone = models.CharField(
        validators=(phone_regex,), unique=True, max_length=10)
    email = models.EmailField()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.phone


class UserOtp(models.Model):
    otp = models.BigIntegerField(blank=True,null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.phone)