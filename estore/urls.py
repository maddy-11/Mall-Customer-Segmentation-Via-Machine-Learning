from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('home/',views.home),
    path('checkout/',views.checkout),
    path('bill',views.bill),
    path('buy/<str:pd>/',views.buy_product),
    path('categories/<str:cat>/',views.p_categories),
    path('cart',views.cart),
    path('login',views.cust_login),
    path('register',views.cust_register),
    path('reviews/<str:pid>/',views.reviews),
    path('delproduct/<str:pid>/',views.delp),
    path('recommended/',views.recommended),
    path('update/',views.update_p),
    path('invoice/',views.invoice),
    path('notifications/<str:pid>/',views.store_notifications),
]
