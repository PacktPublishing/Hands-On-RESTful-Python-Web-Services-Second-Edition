# Run the following code within the Django interactive shell
from datetime import datetime
from django.utils import timezone
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from games.models import Game
from games.serializers import GameSerializer


gamedatetime = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
game1 = Game(name='PAW Patrol: On A Roll!', release_date=gamedatetime, esrb_rating='E (Everyone)')
game1.save()
game2 = Game(name='Spider-Man', release_date=gamedatetime, esrb_rating='T (Teen)')
game2.save()


print(game1.id)
print(game1.name)
print(game1.created_timestamp)
print(game2.id)
print(game2.name)
print(game2.created_timestamp)


game_serializer1 = GameSerializer(game1)
print(game_serializer1.data)


game_serializer2 = GameSerializer(game2)
print(game_serializer2.data)


renderer = JSONRenderer()
rendered_game1 = renderer.render(game_serializer1.data)
rendered_game2 = renderer.render(game_serializer2.data)
print(rendered_game1)
print(rendered_game2)


json_string_for_new_game = '{"name":"Red Dead Redemption 2","release_date":"2018-10-26T01:01:00.776594Z","esrb_rating":"M (Mature)"}'
json_bytes_for_new_game = bytes(json_string_for_new_game, encoding="UTF-8")
stream_for_new_game = BytesIO(json_bytes_for_new_game)
parser = JSONParser()
parsed_new_game = parser.parse(stream_for_new_game)
print(parsed_new_game)


new_game_serializer = GameSerializer(data=parsed_new_game)
if new_game_serializer.is_valid():
    new_game = new_game_serializer.save()
    print(new_game.name)
