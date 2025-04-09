from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItem
from ..products.serializers import ProductSimpleViewSerializer


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "order_date", "status", "delivery_fee", "first_name", "last_name", "email", "state", "city", "delivery_address", "phone_number", "delivery_date", "estimated_delivery"]
        read_only_fields = ["id", "user", "order_date"]


class SimpleOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "status"]
        read_only_fields = ["id", "user"]


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "order", "quantity", "name", "size", "description", "colour", "image1", "price"]
        read_only_fields = ["id", "order"]


class OrderItemSerializerView(ModelSerializer):
    product = ProductSimpleViewSerializer()
    order = SimpleOrderSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "order", "quantity", "name", "size", "description", "colour", "image1", "price"]
        read_only_fields = ["id"]
