from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import *
from game_app.models import Game


# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    wallet = models.PositiveIntegerField(default=0)
    number_of_purchases = models.PositiveIntegerField(default=0,null=True,blank=True)
    history_of_purchases = models.ManyToManyField(to=Game,null=True,blank=True,default=0)
    phone = models.CharField(max_length=20, null=True,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = EmailUserManager()

# Сделать систему скидок от колл покупок