from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Material, NewUser, NewKey, Basket, Orders, Contacts, Delivery, Design, Service, PageRegDescription, ProductName
from django.http import HttpResponse
import bcrypt
import json
from uuid import uuid4
import uuid


class MaterialView(APIView):
    def post(self, request):
        title = request.data.get("title")
        page = request.data.get("page", 1)
        items_per_page = 10
        start_index = (page - 1) * items_per_page
        end_index = page * items_per_page

        materials = Material.objects.filter(title=title)[start_index:end_index]
        output = [
            {
                "id": material.id,
                "title": material.title,
                "name": material.name,
                "img": material.img,
                "brand": material.brand,
                "price": material.price,
                "screenSize": material.screenSize,
                "memoryCard": material.memoryCard,
                "cpu": material.cpu,
                "videoCard": material.videoCard,
            }
            for material in materials
        ]
        return Response(output)


class BasketAdd(APIView):
    def post(self, request):
        key = request.data.get('key')
        basket = Basket.objects.filter(key=key).values('product_id')
        product_ids = [item['product_id'] for item in basket]
        output = []
        materials = Material.objects.filter(id__in=product_ids)
        for material in materials:
            basket = Basket.objects.get(key=key, product_id=material.id)
            for _ in range(basket.quantity):
                output.append({
                    "id": material.id,
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
    title = request.GET.get('title')
    products = Material.objects.filter(title=title,
                                       price__gte=min_price, price__lte=max_price)
    return JsonResponse({'data': list(products.values())})


@csrf_exempt
def new_reg(request):
    post = json.loads(request.body)
    name = post.get('username')
    email = post.get('email')
    hashed_password = bcrypt.hashpw(post.get('password').encode(
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
    if bcrypt.checkpw(post.get('password').encode('utf-8'), new_user.password.encode('utf-8')):
        return HttpResponse(json.dumps({'name': new_user.name, 'key': new_key.key}), status=200)
    else:
        return HttpResponse({'message': 'Wrong password'}, status=401)


@csrf_exempt
def basket(request):
    post = json.loads(request.body)
    key = post.get('key')
    product_id = post.get('product_id')
    quantity = post.get('quantity')
    if quantity == 0:
        basket = Basket.objects.get(key=key, product_id=product_id)
        basket.delete()
    else:
        basket, created = Basket.objects.get_or_create(
            key=key, product_id=product_id, defaults={'quantity': quantity})
        if not created:
            basket.quantity = quantity
            basket.save()
    return HttpResponse(json.dumps({'key': basket.key, 'product_id': basket.product_id, 'quantity': basket.quantity}), status=200)


@csrf_exempt
def orders_list(request):
    post = json.loads(request.body)
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
        for order in orders:
            material = Material.objects.get(id=order.product_id)
            new_id = str(uuid.uuid4())
            for _ in range(int(order.quantity)):
                output.append({
                    "id": new_id,
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


@csrf_exempt
def search(request):
    post = json.loads(request.body)
    name = post.get('name')
    if len(name) >= 3:
        name = name.capitalize()
        matched_materials = Material.objects.filter(name__icontains=name)
        output = [{
            "id": material.id,
            "title": material.title,
            "name": material.name,
            "img": material.img,
            "brand": material.brand,
            "price": material.price,
            "screenSize": material.screenSize,
            "memoryCard": material.memoryCard,
            "cpu": material.cpu,
            "videoCard": material.videoCard,
        } for material in matched_materials]
        return JsonResponse(output, safe=False)
    else:
        return JsonResponse({"message": "Invalid request. Name should be at least 3 characters long."}, status=400)


@csrf_exempt
def contacts(request):
    contacts_list = []
    for contact in Contacts.objects.all():
        contacts_list.append(
            {'name': contact.name, 'contacts': contact.contacts})
    return JsonResponse(contacts_list, safe=False)


@csrf_exempt
def design(request):
    design_list = []
    for designs in Design.objects.all():
        design_list.append({
            'header': designs.header, 'information': designs.information})
    return JsonResponse(design_list, safe=False)


@csrf_exempt
def service(request):
    service_list = []
    for services in Service.objects.all():
        service_list.append(
            {'header': services.header, 'information': services.information})
    return JsonResponse(service_list, safe=False)


@csrf_exempt
def delivery(request):
    delivery_list = []
    for deliverys in Delivery.objects.all():
        delivery_list.append(
            {'header': deliverys.header, 'information': deliverys.information})
    return JsonResponse(delivery_list, safe=False)


@csrf_exempt
def regDescription(request):
    reg_description_list = []
    for reg_descriptions in PageRegDescription.objects.all():
        reg_description_list.append(
            {'header1': reg_descriptions.header1,  'header2': reg_descriptions.header2,
                'span': reg_descriptions.span,  'information': reg_descriptions.information}
        )
    return JsonResponse(reg_description_list, safe=False)


@csrf_exempt
def productName(request):
    products_list = []
    for product in ProductName.objects.all():
        products_list.append(
            {'products': product.products,  'icons': product.icons,
                'title': product.title, }
        )
    return JsonResponse(products_list, safe=False)
