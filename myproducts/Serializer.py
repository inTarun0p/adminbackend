from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "productid", "category", "price", "stock", "sales", "image"]
        read_only_fields = ('id',)
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Get the full URL for the image if it exists
        if instance.image:
            request = self.context.get('request')
            if request is not None:
                representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation

    def create(self, validated_data):
        # Handle file upload
        image = validated_data.pop('image', None)
        product = Product.objects.create(**validated_data)
        
        if image:
            product.image = image
            product.save()
            
        return product