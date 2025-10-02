from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import Restaurant
from .serializers import (
    RestaurantSerializer,
    RestaurantCreateSerializer,
    RestaurantUpdateSerializer
)


class RestaurantListCreateView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Restaurant.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RestaurantCreateSerializer
        return RestaurantSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied('Only admin users can create restaurants.')
        serializer.save()


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RestaurantUpdateSerializer
        return RestaurantSerializer

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can update restaurants.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can delete restaurants.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_restaurants_view(request):

    query = request.GET.get('q', '')
    if not query:
        return Response(
            {'error': 'Query parameter "q" is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    restaurants = Restaurant.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(address__icontains=query),
        is_active=True
    )

    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def available_restaurants_view(request):

    from django.utils import timezone
    from lunch_service.apps.menus.models import Menu
    
    today = timezone.now().date()
    restaurants_with_menu = Restaurant.objects.filter(
        menus__date=today,
        menus__is_active=True,
        is_active=True
    ).distinct()

    serializer = RestaurantSerializer(restaurants_with_menu, many=True)
    return Response(serializer.data)
