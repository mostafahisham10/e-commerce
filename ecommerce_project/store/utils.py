from .models import Customer, Product, Order, OrderItem

def query_data(self):
    if self.request.user.is_authenticated:
        customer = self.request.user.customer
    else:
        device = self.request.COOKIES["device"]
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items    
    return {"order": order, "items": items, "cartItems": cartItems}