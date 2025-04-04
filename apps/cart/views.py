from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .permissions import IsAuthenticatedOrCartItemOwner
from .serializers import CartSerializer, CartItemSerializer, CartItemSerializerView
from rest_framework import viewsets, status
from .pagination import CustomPagination
from .utils import swagger_helper
from ..products.models import Product, ProductSize


class ApiCart(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    pagination = CustomPagination
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @swagger_helper("Cart", "cart")
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @swagger_helper("Cart", "cart")
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @swagger_helper("Cart", "cart")
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @swagger_helper("Cart", "cart")
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)

    @swagger_helper("Cart", "cart")
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ApiCartItem(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    pagination = CustomPagination
    permission_classes = [IsAuthenticatedOrCartItemOwner]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CartItemSerializerView
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.kwargs.get("cart_pk"), cart__user=self.request.user)

    @swagger_helper("CartItem", "cart item")
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @swagger_helper("CartItem", "cart item")
    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        size_id = request.data.get("size")
        quantity = int(request.data.get("quantity"))
        cart_id = self.kwargs.get("cart_pk")

        cart = get_object_or_404(Cart, id=cart_id)
        size = get_object_or_404(ProductSize, id=size_id)
        product = get_object_or_404(Product, id=product_id)

        if product != size.product:
            return Response({"error": "Selected size does not belong to the chosen product."},
                            status=status.HTTP_400_BAD_REQUEST)

        database_quantity = size.quantity
        if database_quantity < 1:
            return Response({"error": "The selected size is out of stock."}, status=status.HTTP_400_BAD_REQUEST)

        # check if quantity is less than that in database
        if quantity > database_quantity > 0:
            quantity = database_quantity

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(quantity=quantity, cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_helper("CartItem", "cart item")
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @swagger_helper("CartItem", "cart item")
    def partial_update(self, request, *args, **kwargs):
        size_id = self.request.data.get("size")
        quantity = request.data.get("quantity")
        cart_item = self.get_object()
        size = get_object_or_404(ProductSize, id=size_id)
        if quantity:
            quantity = int(quantity)

        # size change
        if size and size != cart_item.size:
            size_db_quantity = size.quantity
            if not quantity:
                quantity = cart_item.quantity
            if size_db_quantity <= 0:
                return Response({"error": "The selected size is out of stock."}, status=status.HTTP_400_BAD_REQUEST)
            # if quantity greater than 
            if quantity > size_db_quantity:
                cart_item.size = size
                cart_item.quantity = size_db_quantity
                cart_item.save()

            cart_item.size = size
            cart_item.quantity = quantity
            cart_item.save()
        # quantity change
        if quantity and quantity != cart_item.quantity:
            size_db_quantity = size.quantity
            if size_db_quantity < quantity:
                cart_item.quantity = size_db_quantity
                cart_item.save()
                return Response({"data": f"not enough quantity of item left. you asked for {quantity} but only {size_db_quantity}is left. quantity updated successfully to {quantity}"},status=status.HTTP_200_OK)

            cart_item.quantity = quantity
            cart_item.save()
            return Response({"data": f"quantity updated successfully to {quantity}"}, status=status.HTTP_200_OK)

        # if no params
        return Response({"data": "no change made"}, status=status.HTTP_200_OK)

    @swagger_helper("CartItem", "cart item")
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)
