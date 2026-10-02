from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TankViewSet, ClanViewSet, PlayerViewSet, ModuleViewSet, BattleViewSet

router = DefaultRouter()
router.register(r'tanks', TankViewSet)
router.register(r'clans', ClanViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'battles', BattleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]