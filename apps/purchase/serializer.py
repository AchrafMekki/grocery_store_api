from rest_framework import serializers
from apps.purchase.models import Cart, ItemTest, OrderTest




class CartSerializer(serializers.ModelSerializer):
    cost_per_product = serializers.DecimalField(source='get_cost_per_product', max_digits=4, decimal_places=2, read_only=True)
    total_amount = serializers.DecimalField(source='get_total_amount', max_digits=10, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField()


    class Meta:
        model = Cart
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemTest
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):

    orderItems = serializers.SerializerMethodField(method_name='get_order_items', read_only=True)

    class Meta:
        model = OrderTest
        fields = "__all__"

    def get_order_items(self, obj):
        order_items = obj.orderitems.all()
        serializer = OrderItemSerializer(order_items, many= True)
        return serializer.data