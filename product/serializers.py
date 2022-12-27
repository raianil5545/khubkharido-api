from rest_framework import serializers
from accounts import serializer as user_serializer
from product import services


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    in_stock = serializers.IntegerField()
    brands = serializers.ListField()
    categories = serializers.ListField()
    images = serializers.ImageField()
    created_at = serializers.DateTimeField(read_only=True)
    user = user_serializer.UserSerializers(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return services.ProductDataClass(**data)
