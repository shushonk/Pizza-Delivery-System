from django.db import models
from menu.models import Pizza

class UserBehavior(models.Model):
    session_id = models.CharField(max_length=100)
    pizza_viewed = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True, related_name='viewed_behaviors')
    pizza_ordered = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True, related_name='ordered_behaviors')
    search_query = models.CharField(max_length=200, blank=True)
    category_viewed = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PizzaRecommendation(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    recommended_pizzas = models.JSONField(default=list)
    algorithm_version = models.CharField(max_length=50)
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class PopularPizza(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)
    order_count = models.IntegerField(default=0)
    popularity_score = models.FloatField(default=0)
    time_period = models.CharField(max_length=20)
    calculated_at = models.DateTimeField(auto_now_add=True)