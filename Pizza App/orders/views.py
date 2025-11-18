from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Order, Cart, OrderTracking
from .serializers import (
    OrderSerializer, OrderCreateSerializer, CartSerializer, 
    OrderTrackingSerializer, CartItemSerializer
)
import random
import string

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'session_id'
    
    def create(self, request):
        session_id = request.data.get('session_id')
        if not session_id:
            # Generate session ID if not provided
            session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        cart, created = Cart.objects.get_or_create(
            session_id=session_id,
            defaults={'items': []}
        )
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, session_id=None):
        try:
            cart = Cart.objects.get(session_id=session_id)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        item_serializer = CartItemSerializer(data=request.data)
        if item_serializer.is_valid():
            cart.items.append(item_serializer.validated_data)
            cart.save()
            return Response(CartSerializer(cart).data)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def update_quantity(self, request, session_id=None):
        # Implementation for updating item quantity
        pass

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request):
        # Generate order number
        order_number = f"ORD{timezone.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(order_number=order_number)
            
            # Create initial tracking record
            OrderTracking.objects.create(
                order=order,
                status='pending',
                description='Order placed successfully'
            )
            
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            
            # Update timestamps based on status
            if new_status == 'confirmed' and not order.confirmed_at:
                order.confirmed_at = timezone.now()
            elif new_status == 'delivered' and not order.delivered_at:
                order.delivered_at = timezone.now()
            
            order.save()
            
            # Create tracking record
            OrderTracking.objects.create(
                order=order,
                status=new_status,
                description=request.data.get('description', '')
            )
            
            return Response(OrderSerializer(order).data)
        
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def track(self, request):
        order_number = request.query_params.get('order_number')
        email = request.query_params.get('email')
        
        try:
            order = Order.objects.get(order_number=order_number, customer_email=email)
            tracking_updates = OrderTracking.objects.filter(order=order).order_by('-created_at')
            
            data = {
                'order': OrderSerializer(order).data,
                'tracking': OrderTrackingSerializer(tracking_updates, many=True).data
            }
            return Response(data)
        
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderTrackingViewSet(viewsets.ModelViewSet):
    queryset = OrderTracking.objects.all()
    serializer_class = OrderTrackingSerializer
    filter_backends = []