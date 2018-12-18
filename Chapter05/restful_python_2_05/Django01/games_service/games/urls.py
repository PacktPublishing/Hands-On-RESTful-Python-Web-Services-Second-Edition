from django.conf.urls import url
from games import views

urlpatterns = [
    url(r'^games/$', views.game_collection),
    url(r'^games/(?P<id>[0-9]+)/$', views.game_detail),
]
