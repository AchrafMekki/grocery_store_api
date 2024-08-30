#from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from apps.purchase.models import Cart, OrderTest, ItemTest
from apps.purchase.serializer import CartSerializer, OrderItemSerializer, OrderSerializer
from apps.product.models import Product

#Function-base view
@api_view(['GET']) # by default , it uses a 'GET' method
def view_cart(request):
    # Get all items using ORM
    cart = Cart.objects.all()

    # Deserialize using the CartSerializer
    data = CartSerializer(cart,many=True)

    return Response(data.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = OrderTest.objects.all()

    serializer = OrderSerializer(orders, many=True)

    return Response({'orders': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    order = get_object_or_404(OrderTest, id=pk)

    serializer = OrderSerializer(order, many=False)

    return Response({'order': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):

    user = request.user
    data = request.data

    order_items = data['orderItems']

    if order_items and len(order_items) == 0:
        return Response({
            'error': 'No items in Cart. Please place one product'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        #Create an order
        total_amount = sum(item['price'] * item['quantity'] for item in order_items)

        order = OrderTest.objects.create(
            user=user,
            street=data['street'],
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            phone_no=data['phone_no'],
            country=data['country'],
            total_amount=total_amount
        )

        #Create order items and set order to order items
        for i in order_items:
            product = Product.objects.get(id=i['product'])

            item = ItemTest.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity = i['quantity'],
                price = i['price']
            )

            # Update product stock
            product.stock -= item.quantity
            product.save()
        
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def process_order(request, pk):
    order = get_object_or_404(OrderTest, id=pk)

    order.status = request.data['status']

    serializer = OrderSerializer(order, many=False)

    return Response({'order': serializer.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_order(request, pk):
    order = get_object_or_404(OrderTest, id=pk)

    order.delete()
    return Response({'order': 'Order is deleted.'})