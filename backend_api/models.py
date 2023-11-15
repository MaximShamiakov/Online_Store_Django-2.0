from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Logo(models.Model):
    name = models.CharField(max_length=255)


class Material(models.Model):
    title = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250, blank=True)
    img = models.CharField(max_length=250,  blank=True)
    brand = models.CharField(max_length=250, blank=True)
    price = models.IntegerField(blank=True)
    screenSize = models.CharField(max_length=250, blank=True)
    memoryCard = models.CharField(max_length=250, blank=True)
    cpu = models.CharField(max_length=250, blank=True)
    videoCard = models.CharField(max_length=250, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_materials",
    )


class NewUser(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)


class NewKey(models.Model):
    key = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)


class Basket(models.Model):
    key = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=255, default='')
    quantity = models.PositiveBigIntegerField()


class Orders(models.Model):
    key = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=225)
    quantity = models.CharField(max_length=225)
    lastName = models.CharField(max_length=225)
    firstName = models.CharField(max_length=225)
    patronymic = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    comments = models.CharField(max_length=255, default='')


class Contacts(models.Model):
    name = models.CharField(max_length=225)
    contacts = models.TextField()


class Design(models.Model):
    header = models.CharField(max_length=225)
    information = models.TextField()


class Service(models.Model):
    header = models.CharField(max_length=225)
    information = models.TextField()


class Delivery(models.Model):
    header = models.CharField(max_length=225)
    information = models.TextField()


class PageRegDescription(models.Model):
    header1 = models.CharField(max_length=225)
    header2 = models.CharField(max_length=225)
    span = models.CharField(max_length=225)
    information = models.TextField()


class ProductName(models.Model):
    products = models.CharField(max_length=225)
    icons = models.CharField(max_length=225)
    title = models.CharField(max_length=225)
