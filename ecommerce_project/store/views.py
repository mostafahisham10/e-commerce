from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from .serializers import ProductSerializer
from .utils import query_data
import datetime


class Store(TemplateView):
    template_name = "store/index.html"

    def get_context_data(self, **kwargs):
        data_list = query_data(self)
        products = Product.objects.all()
        context = {"products": products, "cartItems": data_list["cartItems"]}
        return context


class Cart(TemplateView):
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs):
        data_list = query_data(self)
        context = {"order": data_list["order"],
                   "items": data_list["items"], "cartItems": data_list["cartItems"]}
        return context


class Checkout(TemplateView):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
        data_list = query_data(self)
        context = {"order": data_list["order"],
                   "items": data_list["items"], "cartItems": data_list["cartItems"]}
        return context


class UpdateItem(APIView):

    def post(self, request):
        data = request.data
        productId = data["productId"]
        action = data["action"]

        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            device = request.COOKIES["device"]
            customer, created = Customer.objects.get_or_create(device=device)

        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(
            order=order, product=product)

        if action == "add":
            orderItem.quantity += 1
        elif action == "remove":
            orderItem.quantity -= 1
        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return Response("item was added")


class ProcessOrder(APIView):

    def post(self, request):
        data = request.data
        transaction_id = datetime.datetime.now().timestamp()

        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            device = request.COOKIES["device"]
            customer, created = Customer.objects.get_or_create(device=device)
            customer.name = data["form"]["name"]
            customer.email = data["form"]["email"]
            customer.save()

        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True

        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"],
                country=data["shipping"]["country"]
            )

        return Response("order was processed")


class ApiOverview(APIView):

    def get(self, request):
        api_urls = {
            'Products List & Create': 'api/products/',
            'Products Detail, Update & Delete ': 'api/prodcuts/<int:id>/',
        }

        return Response(api_urls)


class ProductListCreate(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ProductDetailUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
