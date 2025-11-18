from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Pizza, Topping, Coupon
from .serializers import (
    CategorySerializer, PizzaSerializer, ToppingSerializer, 
    CouponSerializer, PizzaCreateSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.filter(is_available=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_vegetarian', 'is_spicy', 'crust_type', 'size']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_price', 'created_at']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PizzaCreateSerializer
        return PizzaSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_pizzas = self.queryset.order_by('?')[:8]  # Random 8 pizzas for featured
        serializer = self.get_serializer(featured_pizzas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_suggestions(self, request):
        query = request.query_params.get('q', '')
        if len(query) >= 2:
            suggestions = self.queryset.filter(name__icontains=query)[:5]
            serializer = self.get_serializer(suggestions, many=True)
            return Response(serializer.data)
        return Response([])

class ToppingViewSet(viewsets.ModelViewSet):
    queryset = Topping.objects.filter(is_available=True)
    serializer_class = ToppingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'is_vegetarian', 'is_spicy']
    search_fields = ['name']

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    
    @action(detail=False, methods=['post'])
    def validate(self, request):
        code = request.data.get('code')
        order_amount = request.data.get('order_amount', 0)
        
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            # Check validity
            from django.utils import timezone
            now = timezone.now()
            
            if coupon.valid_from <= now <= coupon.valid_until:
                if order_amount >= coupon.min_order_amount:
                    if coupon.used_count < coupon.usage_limit:
                        return Response({
                            'valid': True,
                            'discount_type': coupon.discount_type,
                            'discount_value': float(coupon.discount_value),
                            'max_discount': float(coupon.max_discount) if coupon.max_discount else None,
                            'message': 'Coupon applied successfully'
                        })
            
            return Response({'valid': False, 'message': 'Invalid or expired coupon'})
        
        except Coupon.DoesNotExist:
            return Response({'valid': False, 'message': 'Coupon not found'})