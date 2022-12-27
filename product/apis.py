from rest_framework import views, response, permissions
from rest_framework import status as rest_status

from accounts import authentication
from . import serializers as product_serializer
from . import services


class ProductCreateListApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = product_serializer.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        serializer.instance = services.create_product(user=request.user, product=data)
        return response.Response(data=serializer.data)

    def get(self, request):
        product_collection = services.get_user_product(user=request.user)
        serializer = product_serializer.ProductSerializer(product_collection, many=True)
        return response.Response(data=serializer.data)


class ProductRetrieveUpdateDelete(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, product_id):
        product_by_id = services.get_product_by_id(product_id=product_id)
        serializer = product_serializer.ProductSerializer(product_by_id)
        return response.Response(data=serializer.data)

    def delete(self, request, product_id):
        services.delete_product_by_id(user=request.user, product_id=product_id)
        return response.Response(status=rest_status.HTTP_204_NO_CONTENT)

    def put(self, request, product_id):
        serializer = product_serializer.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data
        serializer.instance = services.update_product_by_id(user=request.user, product_id=product_id, product_data=product)
        return response.Response(data=serializer.data)

