from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contact, name="contact"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("product/create/", views.product_create, name="product_create"),
]
