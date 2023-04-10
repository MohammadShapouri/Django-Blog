from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserAccount(AbstractUser):
    first_name      = models.CharField(max_length=100, verbose_name="نام")
    last_name       = models.CharField(max_length=100, blank=True, null=True, verbose_name="نام خانوادگی")
    username        = models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name="نام کاربری")
    email           = models.EmailField(max_length=200, unique=True, blank=False, null=False, verbose_name="ایمیل")
    new_email       = models.EmailField(max_length=200, unique=True, blank=True, null=True, verbose_name="ایمیل جدید")
    profile_picture = models.ImageField(default='image/account-image/default/default-profile-pic.jpg', upload_to='image/account-image/', verbose_name="عکس پروفایل")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "حساب کاربری"
        verbose_name_plural = "حساب های کاربری"

    def __str__(self):
        return self.username

    def is_there_any_new_email(self):
        return self.new_email != None # Means there is a new email.

    def is_new_email_validated(self):
        return self.new_email == None # Means it's validated.
