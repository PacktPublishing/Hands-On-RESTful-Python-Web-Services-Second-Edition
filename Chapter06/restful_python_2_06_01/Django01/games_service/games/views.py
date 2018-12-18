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


class EsrbRatingList(generics.ListCreateAPIView):
    queryset = EsrbRating.objects.all()
    serializer_class = EsrbRatingSerializer
    name = 'esrbrating-list'


class EsrbRatingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EsrbRating.objects.all()
    serializer_class = EsrbRatingSerializer
    name = 'esrbrating-detail'


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreList(generics.ListCreateAPIView):
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
            'players': reverse(PlayerList.name, request=request),
            'esrb-ratings': reverse(EsrbRatingList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request)
            })



# from rest_framework.parsers import JSONParser
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from games.models import Game
# from games.serializers import GameSerializer


# @api_view(['GET', 'POST'])
# def game_collection(request):
#     if request.method == 'GET':
#         games = Game.objects.all()
#         games_serializer = GameSerializer(games, many=True)
#         return Response(games_serializer.data)

#     elif request.method == 'POST':
#         game_serializer = GameSerializer(data=request.data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return Response(game_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'POST'])
# def game_detail(request, id):
#     try:
#         game = Game.objects.get(id=id)
#     except Game.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         game_serializer = GameSerializer(game)
#         return Response(game_serializer.data)
#     elif request.method == 'PUT':
#         game_serializer = GameSerializer(game, data=request.data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return Response(game_serializer.data)
#         return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         game.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from rest_framework import status
# from games.models import Game
# from games.serializers import GameSerializer


# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)


# @csrf_exempt
# def game_collection(request):
#     if request.method == 'GET':
#         games = Game.objects.all()
#         games_serializer = GameSerializer(games, many=True)
#         return JSONResponse(games_serializer.data)
#     elif request.method == 'POST':
#         game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return JSONResponse(game_serializer.data, 
#                 status=status.HTTP_201_CREATED)
#         return JSONResponse(game_serializer.errors, 
#             status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# def game_detail(request, id):
#     try:
#         game = Game.objects.get(id=id)
#     except Game.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         game_serializer = GameSerializer(game)
#         return JSONResponse(game_serializer.data)
#     elif request.method == 'PUT':
#         game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(game, 
#             data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return JSONResponse(game_serializer.data)
#         return JSONResponse(game_serializer.errors, 
#             status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         game.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)
