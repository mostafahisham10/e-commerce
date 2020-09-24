from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from .serializers import ProductSerializer
import datetime


class Store(TemplateView):
    template_name = "store/index.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {"get_cart_total": 0,
                     "get_cart_items": 0, "shipping": False}
            cartItems = order["get_cart_items"]

        products = Product.objects.all()
        context = {"products": products, "cartItems": cartItems}
        return context


class Cart(TemplateView):
    template_name = "store/cart.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {"get_cart_total": 0,
                     "get_cart_items": 0, "shipping": False}
            cartItems = order["get_cart_items"]
        context = {"items": items, "order": order, "cartItems": cartItems}
        return context


class Checkout(TemplateView):
    template_name = "store/checkout.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {"get_cart_total": 0,
                     "get_cart_items": 0, "shipping": False}
            cartItems = order["get_cart_items"]
        context = {"items": items, "order": order, "cartItems": cartItems}
        return context


class UpdateItem(APIView):

    def post(self, request):
        data = request.data
        productId = data["productId"]
        action = data["action"]

        print("productId: ", productId)
        print("action: ", action)

        customer = request.user.customer
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
        else:
            print("user is not logged in")

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
