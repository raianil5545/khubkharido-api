from rest_framework import serializers
from product import serializers as product_serializer
from accounts import serializer as user_serializer
from . import services as order_services
from . models import Order


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = product_serializer.ProductSerializer(read_only=True)
    user = user_serializer.UserSerializers(read_only=True)
    name = serializers.CharField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    order_status = serializers.CharField(read_only=True)
    date_placed = serializers.DateTimeField(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data=data)
        return order_services.OrderDataClass(**data)


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
