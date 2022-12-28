from rest_framework import views, permissions, response
from rest_framework import status as rest_status, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from accounts import authentication
from . import serializer as order_serializer
from . import services
from product.models import Product
from .models import Order


class OrderCreateListView(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        data = request.data
        product_id = data["product_id"]
        product = Product.objects.get(id=product_id)
        if not product:
            exceptions.NotFound("Item not found")
        # more checks should be made here
        serializer = order_serializer.OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        serializer.instance = services.create_order(user=request.user, product=product, order=data)
        return response.Response(data=serializer.data)

    def get(self, request):
        order_collection = services.get_user_order(user=request.user)
        serializer = order_serializer.OrderSerializer(order_collection, many=True)
        return response.Response(data=serializer.data)


class OrderRetrieve(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, order_id):
        order = services.get_order_by_id(order_id=order_id)
        serializer = order_serializer.OrderSerializer(order)
        return response.Response(data=serializer.data)


class UpdateOrder(GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = order_serializer.OrderModelSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
