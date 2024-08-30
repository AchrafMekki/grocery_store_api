from rest_framework import serializers
from apps.product.models import Product


class CreateProductSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required=False)

    def validate_stock_check(self, value):
        if value < 0:
            raise serializers.ValidationError("stock must be greater than 0 (positive)")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("price must be grater than 0 (positive)")
        return value

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id',)


class ListProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        #  fields= '__all__'
        exclude = ('stock',)


# json_data = '{"id":1,"name":"Banana","image":"img","price":3,"description":"this is a banana","brand":"Chiquita","stock":2}'