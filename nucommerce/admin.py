from django.contrib import admin

from nucommerce.models import Product, Category,Variant

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Variant)