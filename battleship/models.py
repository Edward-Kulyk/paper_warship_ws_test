# battleship/models.py

from django.db import models

class Game(models.Model):
    game_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Player(models.Model):
    game = models.ManyToManyField(Game, related_name='players')
    name = models.CharField(max_length=100)
    is_turn = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)

class Board(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='board')
    size = models.PositiveIntegerField(default=10)
    state = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ship(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='ships')
    type = models.CharField(max_length=20)
    coordinates = models.JSONField()
    orientation = models.CharField(max_length=20)
    is_sunk = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
