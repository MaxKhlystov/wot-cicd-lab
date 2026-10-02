from rest_framework import serializers
from .models import Tank, Clan, Player, Module, Battle

class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = '__all__'

class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = '__all__'