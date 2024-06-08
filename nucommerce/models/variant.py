from django.db import models

from nucommerce.models import Product


class Variant (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    image = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name