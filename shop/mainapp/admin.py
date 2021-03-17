from django.contrib import admin
from django import forms
from django.forms import ModelChoiceField, ModelForm, ValidationError  # последнее выдает страшные формы с ошибкой
from PIL import Image  # библиотека для работы с изображением
from django.utils.safestring import mark_safe  # обычную строку может преобразовать в строку html (можно делать с ней
# все что позволяет html)
# Register your models here.

from .models import *


class NotebookAdminForm(ModelForm):  # валидатор для изображений (выдает только сообщение с рекомендацией
    # или ошибку при не выполнени рекомендации ) + так же не нужно по ТЗ

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            """<span style = "color: blue; font-size: 10x;">Максимальный размер изображения {}x{}"
            </span>""".format(*Product.MAX_RESOLUTION))

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен привышать 5mb')
        # if img.height < min_height or img.width < min_width:
        #     raise ValidationError('Загруженное изображение меньше допустимого')
        # elif img.height > max_height or img.width > max_width:
        #     raise ValidationError('Загруженное изображение больше допустимого')

        return image


class NotebookAdmin(admin.ModelAdmin):  # исправление для создания новых категорий в админке

    form = NotebookAdminForm  # подключаем функцию валидатора изображений

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):  # исправление для создания новых категорий в админке

    form = NotebookAdminForm  # подключаем функцию валидатора изображений

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
