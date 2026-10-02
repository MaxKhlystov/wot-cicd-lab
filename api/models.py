from django.db import models

class Tank(models.Model):
    TIER_CHOICES = [(i, str(i)) for i in range(1, 11)]
    name = models.CharField(max_length=100, verbose_name="Название танка")
    tank_type = models.CharField(max_length=50, choices=[('HT', 'Тяжелый'), ('MT', 'Средний'), ('LT', 'Легкий'), ('TD', 'ПТ-САУ'), ('SPG', 'Арта')])
    nation = models.CharField(max_length=50, verbose_name="Нация")
    tier = models.IntegerField(choices=TIER_CHOICES, verbose_name="Уровень")

    def __str__(self):
        return f"[{self.tier}] {self.name}"

class Clan(models.Model):
    tag = models.CharField(max_length=10, unique=True, verbose_name="Тег клана")
    name = models.CharField(max_length=100, verbose_name="Название клана")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    def __str__(self):
        return f"[{self.tag}] {self.name}"

class Player(models.Model):
    nickname = models.CharField(max_length=50, unique=True, verbose_name="Никнейм")
    clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Клан")
    battles = models.IntegerField(default=0, verbose_name="Кол-во боев")
    wins = models.IntegerField(default=0, verbose_name="Побед")

    def __str__(self):
        return self.nickname

class Module(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, related_name='modules', verbose_name="Танк")
    name = models.CharField(max_length=100, verbose_name="Название модуля")
    module_type = models.CharField(max_length=50, choices=[('Engine', 'Двигатель'), ('Gun', 'Орудие'), ('Tracks', 'Ходовая')])

    def __str__(self):
        return f"{self.tank.name} - {self.name}"

class Battle(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Игрок")
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, verbose_name="Танк")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата боя")
    damage = models.IntegerField(default=0, verbose_name="Урон")
    is_victory = models.BooleanField(default=False, verbose_name="Победа")

    def __str__(self):
        return f"Бой {self.player.nickname} на {self.tank.name}"