from rest_framework.decorators import api_view
from rest_framework.response import Response
from menu.models import Pizza
from .models import UserBehavior, PizzaRecommendation, PopularPizza
import random

@api_view(['GET'])
def get_recommendations(request):
    session_id = request.query_params.get('session_id', '')
    pizza_id = request.query_params.get('pizza_id', '')
    
    recommendations = []
    
    # If specific pizza ID provided, get similar pizzas
    if pizza_id:
        try:
            # Simple similarity based on same category and characteristics
            pizza = Pizza.objects.get(_id=pizza_id)
            similar_pizzas = Pizza.objects.filter(
                category=pizza.category,
                is_vegetarian=pizza.is_vegetarian,
                is_available=True
            ).exclude(_id=pizza_id)[:4]
            
            from menu.serializers import PizzaSerializer
            recommendations = PizzaSerializer(similar_pizzas, many=True).data
        
        except Pizza.DoesNotExist:
            pass
    
    # If no specific recommendations, show popular pizzas
    if not recommendations:
        popular_pizzas = PopularPizza.objects.filter(
            time_period='weekly'
        ).order_by('-popularity_score')[:6]
        
        if popular_pizzas:
            pizzas = [pp.pizza for pp in popular_pizzas]
            from menu.serializers import PizzaSerializer
            recommendations = PizzaSerializer(pizzas, many=True).data
        else:
            # Fallback: random pizzas
            random_pizzas = Pizza.objects.filter(is_available=True).order_by('?')[:6]
            from menu.serializers import PizzaSerializer
            recommendations = PizzaSerializer(random_pizzas, many=True).data
    
    return Response({
        'recommendations': recommendations,
        'type': 'popular' if not pizza_id else 'similar'
    })

@api_view(['POST'])
def track_user_behavior(request):
    session_id = request.data.get('session_id')
    behavior_type = request.data.get('type')  # view, order, search
    data = request.data.get('data', {})
    
    if behavior_type == 'view' and data.get('pizza_id'):
        UserBehavior.objects.create(
            session_id=session_id,
            pizza_viewed_id=data.get('pizza_id')
        )
    elif behavior_type == 'search' and data.get('query'):
        UserBehavior.objects.create(
            session_id=session_id,
            search_query=data.get('query')
        )
    
    return Response({'status': 'tracked'})