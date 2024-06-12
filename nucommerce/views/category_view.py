from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from nucommerce.models import Category
from nucommerce.serializers import CategorySerializer



class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissions]