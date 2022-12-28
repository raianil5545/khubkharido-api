from django.urls import path

from . import apis


urlpatterns = [
    path("order/", apis.OrderCreateListView.as_view(), name="order-list"),
    path("order/<int:order_id>/", apis.OrderRetrieve.as_view(), name="order"),
    path("order/update/<pk>/", apis.UpdateOrder.as_view(), name="order")
]