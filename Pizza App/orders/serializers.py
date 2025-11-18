from rest_framework import serializers
from .models import Order, Cart, OrderTracking

class CartItemSerializer(serializers.Serializer):
    pizza_id = serializers.CharField()
    pizza_name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    crust_type = serializers.CharField()
    size = serializers.CharField()
    toppings = serializers.ListField(child=serializers.CharField(), required=False)

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = '__all__'

class OrderItemSerializer(serializers.Serializer):
    pizza_id = serializers.CharField()
    pizza_name = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    crust_type = serializers.CharField()
    size = serializers.CharField()
    toppings = serializers.ListField(child=serializers.CharField())

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_number', 'created_at', 'confirmed_at', 'delivered_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['order_number', 'confirmed_at', 'prepared_at', 'delivered_at']

class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = '__all__'