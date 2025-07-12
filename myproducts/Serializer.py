from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name","productid","category","price","stock","sales","image"]
        extra_kwargs = {
            "image": {"required": False},  # Ensures password is write-only and won't be included in responses
        }

    def create(self, validated_data):
        # Create and return a new User instance, given the validated data
        return Product.objects.create(**validated_data)