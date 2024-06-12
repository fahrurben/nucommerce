from django.contrib import admin

from nucommerce.models import CustomUser, Product, Category,Variant

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Variant)