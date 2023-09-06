from django.db import models
# временная зона в которой мы находимся
from django.utils import timezone
# стондартные user django
from django.contrib.auth.models import User


class Material(models.Model):
    # Заголовок материала
    idProduct = models.CharField(max_length=250, blank=True)
    title = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250, blank=True)
    img = models.CharField(max_length=250,  blank=True)
    brand = models.CharField(max_length=250, blank=True)
    price = models.IntegerField(blank=True)
    screenSize = models.CharField(max_length=250, blank=True)
    memoryCard = models.CharField(max_length=250, blank=True)
    cpu = models.CharField(max_length=250, blank=True)
    videoCard = models.CharField(max_length=250, blank=True)

    # Слаг - это унекальн индефикатор обьекта
    # slaug = models.SlugField(max_length=255, unique_for_date="publish")
    # даты публикации
    # добовляем timezone.now
    publish = models.DateTimeField(default=timezone.now)
    # пробивает дату запроса
    updated = models.DateTimeField(auto_now=True)
    # пробивает когда обьект добавляется в базу данных
    created = models.DateTimeField(auto_now_add=True)
    # Автор творения
    author = models.ForeignKey(
        # User - указывает таблицу связанную с нашим полем
        User,
        # on_delete=models.CASCADE - при удалении пользывотеля, удаляются все его мотериалы
        on_delete=models.CASCADE,
        # related_name='user_materials' - получение всех материалов у автора к которым он имеет отнашения
        related_name="user_materials",
    )


class NewUser(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=30)


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
