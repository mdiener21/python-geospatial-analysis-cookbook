from django.shortcuts import render


def route_map(request):
    return render(request, 'route-map.html')