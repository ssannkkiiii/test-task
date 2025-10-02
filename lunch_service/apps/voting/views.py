from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Q
from .models import Vote, VotingResult
from .serializers import (
    VoteSerializer,
    VoteCreateSerializer,
    VotingResultSerializer,
    TodayVoteSerializer,
    VoteStatsSerializer
)


class VoteListCreateView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VoteCreateSerializer
        return VoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def vote_for_restaurant_view(request, menu_id):

    from lunch_service.apps.menus.models import Menu
    
    try:
        menu = Menu.objects.get(id=menu_id, is_active=True)
    except Menu.DoesNotExist:
        return Response(
            {'error': 'Menu not found or inactive.'},
            status=status.HTTP_404_NOT_FOUND
        )

    today = timezone.now().date()
    
    existing_vote = Vote.objects.filter(user=request.user, date=today).first()
    if existing_vote:
        return Response(
            {'error': 'You have already voted for today.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if menu.date != today:
        return Response(
            {'error': 'Can only vote for today\'s menu.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    vote = Vote.objects.create(
        user=request.user,
        menu=menu,
        date=today
    )

    serializer = VoteSerializer(vote)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def today_vote_view(request):

    today = timezone.now().date()
    try:
        vote = Vote.objects.get(user=request.user, date=today)
        serializer = TodayVoteSerializer(vote)
        return Response(serializer.data)
    except Vote.DoesNotExist:
        return Response(
            {'message': 'No vote found for today.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def today_results_view(request):
  
    today = timezone.now().date()
    
    voting_result = VotingResult.get_or_create_for_date(today)
    
    user_vote = Vote.objects.filter(user=request.user, date=today).first()
    user_vote_data = None
    if user_vote:
        user_vote_data = TodayVoteSerializer(user_vote).data

    response_data = {
        'date': today,
        'total_votes': voting_result.total_votes,
        'user_voted': user_vote is not None,
        'user_vote': user_vote_data,
        'results': voting_result.results
    }

    serializer = VoteStatsSerializer(response_data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def results_for_date_view(request, date):
    
    try:
        voting_result = VotingResult.get_or_create_for_date(date)
        serializer = VotingResultSerializer(voting_result)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Error retrieving results: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_voting_history_view(request):
  
    votes = Vote.objects.filter(user=request.user).order_by('-date')
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def cancel_today_vote_view(request):
    
    today = timezone.now().date()
    try:
        vote = Vote.objects.get(user=request.user, date=today)
        vote.delete()
        return Response(
            {'message': 'Vote cancelled successfully.'},
            status=status.HTTP_200_OK
        )
    except Vote.DoesNotExist:
        return Response(
            {'error': 'No vote found for today.'},
            status=status.HTTP_404_NOT_FOUND
        )
