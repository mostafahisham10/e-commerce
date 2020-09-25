from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device
        return str(name)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    digital = models.BooleanField(default=False, blank=True)
    image = models.ImageField(default="../static/images/default.png")

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    @property
    # Is Cart digital
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for item in order_items:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    # Cart tota price
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    # Cart total items
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name

    @property
    # Item total price
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.address
