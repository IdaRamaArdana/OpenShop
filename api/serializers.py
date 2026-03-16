from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'shop', 'price', 'sku', 'description', 
            'location', 'discount', 'category', 'stock', 
            'is_available', 'picture', 'is_delete', '_links'
        ]

    def get__links(self, obj):
        request = self.context.get('request')
        if request:
            base_url = request.build_absolute_uri('/')[:-1]
        else:
            base_url = "http://localhost:8000"

        return [
            {
                "rel": "self",
                "href": f"{base_url}/products",
                "action": "POST",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "GET",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "PUT",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "DELETE",
                "types": ["application/json"]
            }
        ]