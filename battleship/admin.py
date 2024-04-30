# battleship/admin.py

from django.contrib import admin
from .models import Game, Player, Board, Ship

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Board)
admin.site.register(Ship)
