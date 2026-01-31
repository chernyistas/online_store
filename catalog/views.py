from typing import Optional

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import ContactInfo, Product

from .forms import ProductForm


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу каталога."""
    all_products = Product.objects.order_by("-created_at")
    paginator = Paginator(all_products, 6)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "catalog/home.html", {"page_obj": page_obj})


def contact(request: HttpRequest) -> HttpResponse:
    """Страница контактов с формой обратной связи."""
    if request.method == "POST":
        name: Optional[str] = request.POST.get("name")
        phone: Optional[str] = request.POST.get("phone")
        message: Optional[str] = request.POST.get("message")

        if name and message:
            ContactInfo.objects.create(
                name=f"Заявка: {name}",
                email="feedback@store.ru",
                phone=phone or "",
                address=message[:255],
            )
            contact_phone = phone or "email"
            messages.success(request, f"Спасибо {name}! Свяжемся по {contact_phone}")
            return redirect("catalog:contact")

    context = {
        "store_contacts": {
            "name": "Online Store",
            "email": "feedback@store.ru",
            "phone": "8-098-765-43-21",
            "address": "Московская область, Мытищи, улица Самая Хорошая",
        },
    }
    return render(request, "catalog/contact.html", context)


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """отображает страницу с подробной информацией о товаре"""
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)


def product_create(request: HttpRequest) -> HttpResponse:
    """Создание нового продукта через форму"""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("catalog:product_detail", pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {"form": form})
