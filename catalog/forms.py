from django import forms

from .models import Category, Product


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования товаров"""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["category"].empty_label = "Выберите категорию"
