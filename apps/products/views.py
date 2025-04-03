from django.shortcuts import render
from .pagination import CustomPagination
from .serializers import ProductCategorySerializer, ProductSubCategorySerializer, ProductSerializer, \
    ProductSizeSerializer, ProductViewSerializer, ProductSubCategoryViewSerializer, ProductCategoryDetailSerializer, \
    ProductSizeViewSerializer
from .models import Product, ProductSubCategory, ProductCategory, ProductSize
from rest_framework import viewsets
from .utils import swagger_helper


class ApiProductCategory(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    queryset = ProductCategory.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductCategoryDetailSerializer
        return ProductCategorySerializer

    @swagger_helper(tags="ProductCategory", model="Product category")
    def list(self, *args, **kwargs):
        return super().list(self, *args, **kwargs)

    @swagger_helper(tags="ProductCategory", model="Product category")
    def retrieve(self, *args, **kwargs):
        return super().create(self, *args, **kwargs)

    @swagger_helper(tags="ProductCategory", model="Product category")
    def create(self, *args, **kwargs):
        return super().create(self, *args, **kwargs)

    @swagger_helper(tags="ProductCategory", model="Product category")
    def partial_update(self, *args, **kwargs):
        return super().partial_update(self, *args, **kwargs)

    @swagger_helper(tags="ProductCategory", model="Product category")
    def destroy(self, *args, **kwargs):
        return super().destroy(self, *args, **kwargs)


class ApiProductSubCategory(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    queryset = ProductSubCategory.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSubCategoryViewSerializer
        return ProductSubCategorySerializer

    @swagger_helper(tags="ProductSubCategory", model="Product sub category")
    def list(self, *args, **kwargs):
        return super().list(self, *args, **kwargs)

    @swagger_helper(tags="ProductSubCategory", model="Product sub category")
    def retrieve(self, *args, **kwargs):
        return super().create(self, *args, **kwargs)

    @swagger_helper(tags="ProductSubCategory", model="Product sub category")
    def create(self, *args, **kwargs):
        return super().create(self, *args, **kwargs)

    @swagger_helper(tags="ProductSubCategory", model="Product sub category")
    def partial_update(self, *args, **kwargs):
        return super().partial_update(self, *args, **kwargs)

    @swagger_helper(tags="ProductSubCategory", model="Product sub category")
    def destroy(self, *args, **kwargs):
        return super().destroy(self, *args, **kwargs)


class ApiProduct(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductViewSerializer
        return ProductSerializer

    @swagger_helper(tags="Product", model="Product")
    def list(self, *args, **kwargs):
        return super().list(self, *args, **kwargs)

    @swagger_helper(tags="Product", model="Product")
    def retrieve(self, *args, **kwargs):
        return super().create(self, *args, **kwargs)

    @swagger_helper(tags="Product", model="Product")
    def create(self, *args, **kwargs):
        return super().create(self, *args, **kwargs)

    @swagger_helper(tags="Product", model="Product")
    def partial_update(self, *args, **kwargs):
        return super().partial_update(self, *args, **kwargs)

    @swagger_helper(tags="Product", model="Product")
    def destroy(self, *args, **kwargs):
        return super().destroy(self, *args, **kwargs)


class ApiProductSize(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    queryset = ProductSize.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSizeViewSerializer
        return ProductSizeSerializer

    @swagger_helper(tags="ProductSize", model="Product size")
    def list(self, *args, **kwargs):
        return super().list(self, *args, **kwargs)

    @swagger_helper(tags="ProductSize", model="Product size")
    def retrieve(self, *args, **kwargs):
        return super().create(self, *args, **kwargs)

    @swagger_helper(tags="ProductSize", model="Product size")
    def create(self, *args, **kwargs):
        return super().create(self, *args, **kwargs)

    @swagger_helper(tags="ProductSize", model="Product size")
    def partial_update(self, *args, **kwargs):
        return super().partial_update(self, *args, **kwargs)

    @swagger_helper(tags="ProductSize", model="Product size")
    def destroy(self, *args, **kwargs):
        return super().destroy(self, *args, **kwargs)