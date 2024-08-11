from rest_framework import serializers
from nucommerce.models import UploadImageModel

class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImageModel
        fields = '__all__'