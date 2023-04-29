from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    account = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'category': {'required': False},
            'barcode': {'required': False},
            'size': {'required': False},
            'name': {'required': False},
        }

