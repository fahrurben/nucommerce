from rest_framework import serializers

from nucommerce.models import Category
from django.utils.text import slugify
from django.db.models import Q

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

    def validate_name(self, value):
        check_name = False
        if self.instance is None:
            check_name = Category.objects.filter(slug=slugify(value)).exists()
        else:
            check_name = Category.objects.filter(~Q(id=self.instance.id), slug=slugify(value)).exists()

        if check_name:
            raise serializers.ValidationError(f'Category with name {value} already exist')

        return value

    def create(self, validated_data):
        slug = slugify(validated_data.get('name'))
        return Category.objects.create(slug=slug, **validated_data)

    def update(self, instance, validated_data):
        slug = slugify(validated_data.get('name'))
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slug
        instance.save()
        return instance
