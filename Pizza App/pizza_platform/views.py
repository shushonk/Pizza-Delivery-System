from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def menu(request):
    return render(request, 'menu.html')

def cart(request):
    return render(request, 'cart.html')

def deals(request):
    return render(request, 'deals.html')

def track(request):
    return render(request, 'track.html')