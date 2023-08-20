from django.shortcuts import render
from rest_framework.views import APIView
from .models import Material
from rest_framework.response import Response
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewUser, NewKey, Basket, Orders
from django.http import HttpResponse
import bcrypt
import json
from uuid import uuid4
import uuid


class MaterialView(APIView):
    def post(self, request):
        output = [
            {
                "idProduct": output.idProduct,
                "title": output.title,
                "name": output.name,
                "img": output.img,
                "brand": output.brand,
                "price": output.price,
                "screenSize": output.screenSize,
                "memoryCard": output.memoryCard,
                "cpu": output.cpu,
                "videoCard": output.videoCard,
            }
            for output in Material.objects.all()
        ]
        return Response(output)


class BasketAdd(APIView):
    def post(self, request):
        post = json.loads(request.body)
        key = post.get('key')
        basket = Basket.objects.filter(key=key).values('product_id')
        product_ids = [item['product_id'] for item in basket]

        output = []
        materials = Material.objects.filter(idProduct__in=product_ids)
        for material in materials:
            basket = Basket.objects.get(key=key, product_id=material.idProduct)
            if 1 <= basket.quantity:
                for _ in range(basket.quantity):
                    output.append({
                        "id": material.idProduct,
                        "title": material.title,
                        "name": material.name,
                        "img": material.img,
                        "brand": material.brand,
                        "price": material.price,
                        "screenSize": material.screenSize,
                        "memoryCard": material.memoryCard,
                        "cpu": material.cpu,
                        "videoCard": material.videoCard,
                    })
        return Response(output)


def get_filtered_products(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    products = Material.objects.filter(
        Q(price__gte=min_price) & Q(price__lte=max_price))

    return JsonResponse({'data': list(products.values())})


@csrf_exempt
def new_reg(request):
    post = json.loads(request.body)
    name = post.get('username')
    email = post.get('email')
    password = post.get('password')
    hashed_password = bcrypt.hashpw(password.encode(
        'utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = NewUser(email=email, password=hashed_password, name=name)
    new_user.save()
    key = str(uuid4())
    new_key = NewKey(user=new_user, key=key)
    new_key.save()
    return HttpResponse(json.dumps({'key': new_key.key, 'name': new_user.name}), status=201)


@csrf_exempt
def new_login(request):
    post = json.loads(request.body)
    email = post.get('email')
    password = post.get('password')
    new_user = None
    try:
        new_user = NewUser.objects.get(email=email)
    except Exception:
        return HttpResponse({'message': 'User not found'}, status=401)
    new_key = None
    try:
        new_key = NewKey.objects.get(user=new_user)
    except Exception:
        return HttpResponse({'message': 'User key not found'}, status=401)
    if bcrypt.checkpw(password.encode('utf-8'), new_user.password.encode('utf-8')):
        return HttpResponse(json.dumps({'name': new_user.name, 'key': new_key.key}), status=200)
    else:
        return HttpResponse({'message': 'Wrong password'}, status=401)


@csrf_exempt
def basket(request):
    post = json.loads(request.body)
    key = post.get('key')
    product_id = post.get('product_id')
    quantity = post.get('quantity')
    if quantity == 0:  # если количество равно 0, то удаляем модель из базы
        # try:
        basket = Basket.objects.get(key=key, product_id=product_id)
        basket.delete()
        # except Basket.DoesNotExist:
        #     pass
    else:  # если количество не равно 0, то обновляем или создаем модель в базе
        basket, created = Basket.objects.get_or_create(
            key=key, product_id=product_id, defaults={'quantity': quantity})
        if not created:
            basket.quantity = quantity
            basket.save()
    return HttpResponse(json.dumps({'key': basket.key, 'product_id': basket.product_id, 'quantity': basket.quantity}), status=200)


@csrf_exempt
def orders_list(request):
    # if request.method == 'POST':
    post = json.loads(request.body)
    # print(post)
    key = post.get('key')
    product_id = post.get('product_id')
    quantity = post.get('quantity')
    lastName = post.get('lastName')
    firstName = post.get('firstName')
    patronymic = post.get('patronymic')
    phone = post.get('phone')
    email = post.get('email')
    city = post.get('city')
    address = post.get('address')
    comments = post.get('comment')

    Orders.objects.create(
        key=key,
        product_id=product_id,
        quantity=quantity,
        lastName=lastName,
        firstName=firstName,
        patronymic=patronymic,
        phone=phone,
        email=email,
        city=city,
        address=address,
        comments=comments
    )

    return HttpResponse(json.dumps({'success': True}), status=200)


class AddOrders(APIView):
    def post(self, request):
        post_data = json.loads(request.body)
        key = post_data.get('key')
        orders = Orders.objects.filter(key=key)
        output = []
        if orders.exists():
            for order in orders:
                material = Material.objects.get(idProduct=order.product_id)
                new_id = str(uuid.uuid4())
                for _ in range(int(order.quantity)):
                    output.append({
                        "idProduct": new_id,
                        "title": material.title,
                        "name": material.name,
                        "img": material.img,
                        "brand": material.brand,
                        "price": material.price,
                        "screenSize": material.screenSize,
                        "memoryCard": material.memoryCard,
                        "cpu": material.cpu,
                        "videoCard": material.videoCard,
                        "lastName": order.lastName,
                        "firstName": order.firstName,
                        "patronymic": order.patronymic,
                        "phone": order.phone,
                        "email": order.email,
                        "city": order.city,
                        "address": order.address,
                        "comments": order.comments,
                    })
        return Response(output)