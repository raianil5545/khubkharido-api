from rest_framework import serializers
from . import services


class UserSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return services.UserDataClass(**data)