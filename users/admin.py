from django.contrib import admin
from users.models import CustomUser, UserOtp
from django.contrib.auth.models import  Group
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserOtp)
admin.site.unregister(Group)