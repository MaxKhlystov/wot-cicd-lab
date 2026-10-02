from rest_framework import viewsets
from .models import Tank, Clan, Player, Module, Battle
from .serializers import TankSerializer, ClanSerializer, PlayerSerializer, ModuleSerializer, BattleSerializer

# Каждый ViewSet автоматически дает 5 endpoints: list, create, retrieve, update, partial_update, destroy
# 5 моделей * 4 основные CRUD операции = 20 CRUD операций!

class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer

class ClanViewSet(viewsets.ModelViewSet):
    queryset = Clan.objects.all()
    serializer_class = ClanSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer