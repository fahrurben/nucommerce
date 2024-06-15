from django.db import models

from nucommerce.models import Category


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField()
    thumbnail = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

