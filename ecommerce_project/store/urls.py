from django.urls import path
from .views import (Store, Cart, Checkout, UpdateItem, ProcessOrder,
                    ApiOverview, ProductListCreate, ProductDetailUpdateDelete)

urlpatterns = [
    path('', Store.as_view(), name='store'),
    path('cart/', Cart.as_view(), name='cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('update-item/', UpdateItem.as_view(), name="update_item"),
    path('process-order/', ProcessOrder.as_view(), name="process_order"),
    path('api/', ApiOverview.as_view(), name='api_overview'),
    path('api/products/', ProductListCreate.as_view(), name='products_view'),
    path('api/products/<int:id>/',
         ProductDetailUpdateDelete.as_view(), name='products_detail_view')
]
