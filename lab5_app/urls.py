from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("contacts", views.contacts, name="contacts"),
    path("shop", views.shop, name="shop"),
    path("shop/item/<int:dish_id>", views.shop_item_dish, name="shop_item_dish"),
    path("shop/item/add", views.shop_item_add, name="shop_item_add"),
    path("cart", views.cart, name="cart"),
    path("order/del", views.order_del, name="order_del"),
]