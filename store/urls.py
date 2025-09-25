from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("profile/", views.profile_view, name="profile"),
    path('', views.product_list, name='product_list'),
    path('api/products/', views.api_products, name='api_products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_details, name="cart_details"),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('order/confirmed/<int:order_id>/', views.order_confirmed, name='order_confirmed'),
    path('contact/', views.contact, name='contact'),
]
