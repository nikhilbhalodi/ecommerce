from django.urls import path
from .views import ProductDetailView,ProductView,add_to_cart,remove_from_cart,remove_single_product_from_cart,OrderSummaryView
from .views import subscribe
app_name= 'app1'

urlpatterns = [
    path('', ProductView.as_view(), name='home'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart , name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-product-from-cart/<slug>/', remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    
]
