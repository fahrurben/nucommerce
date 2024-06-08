from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(default="", null=False, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name