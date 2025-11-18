from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PizzaViewSet, ToppingViewSet, CouponViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'pizzas', PizzaViewSet)
router.register(r'toppings', ToppingViewSet)
router.register(r'coupons', CouponViewSet)

urlpatterns = [
    path('', include(router.urls)),
]