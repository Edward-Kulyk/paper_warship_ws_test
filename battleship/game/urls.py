from django.urls import path, include

from .views import home, new_game, join_game,game

urlpatterns = [
    path("", home, name="home"),
    path("game/<str:game_id>/", game, name="game"),
    path("new_game/", new_game),
    path("join_game/", join_game),
]