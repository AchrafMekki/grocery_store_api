from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import CreateProductSerializer, ListProductSerializer
from .models import Product


# List all products

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    data = ListProductSerializer(products, many=True)
    return Response(data.data, status=status.HTTP_200_OK)

# Who can create products? Only superuser?

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_product(request):
    data = request.data
    product = CreateProductSerializer(data=data)
        
    product.is_valid()
    saved_product = product.save()

    return Response({"name": saved_product.name}, status=status.HTTP_201_CREATED)
