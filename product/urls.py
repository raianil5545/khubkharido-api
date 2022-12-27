from django.urls import path

from . import apis

urlpatterns = [
    path("product/", apis.ProductCreateListApi.as_view(), name="product"),
    path("product/<int:product_id>/", apis.ProductRetrieveUpdateDelete.as_view(), name="product_detail")
]