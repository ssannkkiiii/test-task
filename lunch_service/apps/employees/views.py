from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import EmployeeProfile
from .serializers import (
    EmployeeProfileSerializer,
    EmployeeProfileCreateSerializer,
    EmployeeListSerializer
)


class EmployeeListCreateView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeProfile.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeProfileCreateSerializer
        return EmployeeListSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return Response(
                {'error': 'Only admin users can create employees.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can update employees.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can delete employees.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_employees_view(request):
    query = request.GET.get('q', '')
    if not query:
        return Response(
            {'error': 'Query parameter "q" is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    employees = EmployeeProfile.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(employee_id__icontains=query) |
        Q(department__icontains=query),
        is_active=True
    )

    serializer = EmployeeListSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_profile_view(request):

    try:
        employee_profile = request.user.employee_profile
        serializer = EmployeeProfileSerializer(employee_profile)
        return Response(serializer.data)
    except EmployeeProfile.DoesNotExist:
        return Response(
            {'error': 'Employee profile not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
