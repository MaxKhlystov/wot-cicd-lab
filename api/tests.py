from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Tank, Player

class WoTAPITests(APITestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name="IS-7", tank_type="HT", nation="USSR", tier=10)
        self.player = Player.objects.create(nickname="TestPlayer", battles=100, wins=55)

    def test_get_tanks_list(self):
        """Тест получения списка танков (Read)"""
        response = self.client.get('/api/tanks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_player(self):
        """Тест создания игрока (Create)"""
        data = {"nickname": "NewPlayer", "battles": 0, "wins": 0}
        response = self.client.post('/api/players/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 2)

    def test_update_tank(self):
        """Тест обновления танка (Update)"""
        data = {"name": "IS-7", "tank_type": "HT", "nation": "USSR", "tier": 10}
        response = self.client.put(f'/api/tanks/{self.tank.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)