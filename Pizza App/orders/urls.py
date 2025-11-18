from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CartViewSet, OrderTrackingViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'carts', CartViewSet)
router.register(r'tracking', OrderTrackingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]