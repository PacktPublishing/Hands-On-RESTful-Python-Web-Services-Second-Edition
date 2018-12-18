from games.models import EsrbRating
from games.models import Game
from games.models import Player
from games.models import PlayerScore
from games.serializers import EsrbRatingSerializer
from games.serializers import GameSerializer
from games.serializers import PlayerSerializer
from games.serializers import PlayerScoreSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework import permissions
from games.serializers import UserSerializer
from games.customized_permissions import IsOwnerOrReadOnly
from rest_framework import filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from django_filters.rest_framework import FilterSet
from rest_framework.throttling import ScopedRateThrottle


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class EsrbRatingList(generics.ListCreateAPIView):
    throttle_scope = 'esrb-ratings'
    throttle_classes = (ScopedRateThrottle,)
    filterset_fields = ('description',)
    search_fields = ('^description',)
    ordering_fields = ('description',)
    queryset = EsrbRating.objects.all()
    serializer_class = EsrbRatingSerializer
    name = 'esrbrating-list'


class EsrbRatingDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_scope = 'esrb-ratings'
    throttle_classes = (ScopedRateThrottle,)
    queryset = EsrbRating.objects.all()
    serializer_class = EsrbRatingSerializer
    name = 'esrbrating-detail'


class GameList(generics.ListCreateAPIView):
    filterset_fields = (
        'name', 
        'esrb_rating', 
        'release_date', 
        'played_times',
        'owner',)
    search_fields = (
        '^name',)
    ordering_fields = (
        'name',
        'release_date',
        'played_times',)
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly)


class PlayerList(generics.ListCreateAPIView):
    filterset_fields = (
        'name', 
        'gender',)
    search_fields = (
        '^name',)
    ordering_fields = (
        'name',)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'



class PlayerScoreFilter(FilterSet):
    player_name = AllValuesFilter(field_name='player__name')
    game_name = AllValuesFilter(field_name='game__name')
    min_score = NumberFilter(field_name='score', lookup_expr='gte')
    max_score = NumberFilter(field_name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(field_name='score_date', lookup_expr='gte')
    to_score_date = DateTimeFilter(field_name='score_date', lookup_expr='lte')

    class Meta:
        model = PlayerScore
        fields = (
            'game_name',
            'player_name',
            'score',
            'from_score_date',
            'to_score_date',
            'min_score',
            'max_score',)


class PlayerScoreList(generics.ListCreateAPIView):
    ordering_fields = (
        'score',
        'score_date',)
    filterset_class = PlayerScoreFilter
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse(UserList.name, request=request),
            'players': reverse(PlayerList.name, request=request),
            'esrb-ratings': reverse(EsrbRatingList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request)
            })
