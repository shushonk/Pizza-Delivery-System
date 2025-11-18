from django.urls import path
from .views import get_recommendations, track_user_behavior

urlpatterns = [
    path('get-recommendations/', get_recommendations, name='get_recommendations'),
    path('track-behavior/', track_user_behavior, name='track_behavior'),
]