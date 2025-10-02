from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Menu, MenuItem
from .serializers import (
    MenuSerializer,
    MenuCreateSerializer,
    MenuListSerializer,
    TodayMenuSerializer,
    MenuItemSerializer,
    MenuItemCreateSerializer
)


class MenuListCreateView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Menu.objects.filter(is_active=True)
        
        restaurant_id = self.request.query_params.get('restaurant')
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MenuCreateSerializer
        return MenuListSerializer

    def perform_create(self, serializer):

        if not self.request.user.is_staff:
            return Response(
                {'error': 'Only admin users can create menus.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can update menus.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can delete menus.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def today_menu_view(request):

    today = timezone.now().date()
    menus = Menu.objects.filter(date=today, is_active=True)
    
    serializer = TodayMenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def restaurant_today_menu_view(request, restaurant_id):

    today = timezone.now().date()
    try:
        menu = Menu.objects.get(
            restaurant_id=restaurant_id,
            date=today,
            is_active=True
        )
        serializer = TodayMenuSerializer(menu)
        return Response(serializer.data)
    except Menu.DoesNotExist:
        return Response(
            {'error': 'No menu available for this restaurant today.'},
            status=status.HTTP_404_NOT_FOUND
        )


class MenuItemListCreateView(generics.ListCreateAPIView):

    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        menu_id = self.kwargs.get('menu_id')
        return MenuItem.objects.filter(menu_id=menu_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MenuItemCreateSerializer
        return MenuItemSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return Response(
                {'error': 'Only admin users can create menu items.'},
                status=status.HTTP_403_FORBIDDEN
            )
        menu_id = self.kwargs.get('menu_id')
        serializer.save(menu_id=menu_id)


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        menu_id = self.kwargs.get('menu_id')
        return MenuItem.objects.filter(menu_id=menu_id)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can update menu items.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can delete menu items.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
