from rest_framework import serializers

from django.utils.text import slugify
from django.db.models import Q

from nucommerce.models import Product, Variant, Category
from nucommerce.serializers import CategorySerializer

class VariantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    slug = serializers.SlugField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Variant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = CategorySerializer(required=False)
    category_id = serializers.IntegerField()
    slug = serializers.SlugField(read_only=True)
    variant_set = VariantSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = ('id', 'category_id', 'category', 'name', 'slug', 'description', 'thumbnail', 'variant_set')

    def validate_name(self, value):
        check_name = False
        if self.instance is None:
            check_name = Product.objects.filter(slug=slugify(value)).exists()
        else:
            check_name = Product.objects.filter(~Q(id=self.instance.id), slug=slugify(value)).exists()

        if check_name:
            raise serializers.ValidationError(f'Product with name {value} already exist')

        return value

    def create(self, validated_data):
        variant_set = validated_data.pop('variant_set')
        slug = slugify(validated_data.get('name'))
        category = Category.objects.get(id=validated_data.get('category_id'))
        product = Product.objects.create(slug=slug, **validated_data)
        product.category = category
        product.save()
        if variant_set:
            for variant in variant_set:
                variant_slug = slugify(variant.get('name'))
                Variant.objects.create(product=product, slug=variant_slug, **variant)
        return product

    def update(self, instance, validated_data):
        variant_set = validated_data.pop('variant_set')
        slug = slugify(validated_data.get('name'))
        category = Category.objects.get(id=validated_data.get('category_id'))
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slug
        instance.category = category
        instance.description = validated_data.get('description', instance.description)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)

        if variant_set:
            updated_variant_ids = []
            for variant in variant_set:
                variant_slug = slugify(variant.get('name'))
                if variant.get('id') is None:
                    Variant.objects.create(product=instance, slug=variant_slug, **variant)
                else:
                    updated_variant_ids.append(variant.get('id'))
                    variant_instance = Variant.objects.get(id=variant.get('id'))
                    variant_instance.name = variant.get('name', variant_instance.name)
                    variant_instance.slug = variant_slug
                    variant_instance.image = variant.get('image', variant_instance.image)
                    variant_instance.price = variant.get('price', variant_instance.price)
                    variant_instance.stock = variant.get('stock', variant_instance.stock)
                    variant_instance.save()

            deleted_variants = Variant.objects.filter(product=instance).exclude(id__in=updated_variant_ids).all()
            for deleted_variant in deleted_variants:
                deleted_variant.delete()
        instance.save()
        return instance