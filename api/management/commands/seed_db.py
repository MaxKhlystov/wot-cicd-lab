from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Tank, Clan, Player, Module, Battle


class Command(BaseCommand):
    help = 'Наполняет базу данных тестовыми данными World of Tanks'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Очистка старых данных...')
        # Удаляем в порядке зависимостей
        Battle.objects.all().delete()
        Module.objects.all().delete()
        Player.objects.all().delete()
        Clan.objects.all().delete()
        Tank.objects.all().delete()

        self.stdout.write('Создание танков...')
        tanks_data = [
            ('IS-7', 'HT', 'USSR', 10),
            ('E 100', 'HT', 'Germany', 10),
            ('M103', 'HT', 'USA', 10),
            ('T-54 first prototype', 'MT', 'USSR', 8),
            ('Leopard 1', 'MT', 'Germany', 8),
            ('Patton', 'MT', 'USA', 6),
            ('AMX 13 90', 'LT', 'France', 8),
            ('T2 Light Tank', 'LT', 'USA', 2),
            ('Object 268', 'TD', 'USSR', 10),
            ('G.W. Panther', 'SPG', 'Germany', 8),
        ]
        tanks = {}
        for name, ttype, nation, tier in tanks_data:
            tanks[name] = Tank.objects.create(
                name=name, tank_type=ttype, nation=nation, tier=tier
            )

        self.stdout.write('Создание кланов...')
        clans_data = [
            ('RUS', 'Red Storm', 1520),
            ('DEU', 'Panzer Division', 1480),
            ('USA', 'Liberty', 1390),
        ]
        clans = {}
        for tag, name, rating in clans_data:
            clans[tag] = Clan.objects.create(tag=tag, name=name, rating=rating)

        self.stdout.write('Создание игроков...')
        players_data = [
            ('Sniper_1945', 'RUS', 5200, 3120),
            ('TigerAce', 'DEU', 4800, 2640),
            ('LibertyBell', 'USA', 3900, 1950),
            ('ReklessRomeo', 'RUS', 2100, 1050),
            ('Noob228', None, 350, 90),
        ]
        players = {}
        for nick, clan_tag, battles, wins in players_data:
            players[nick] = Player.objects.create(
                nickname=nick,
                clan=clans.get(clan_tag) if clan_tag else None,
                battles=battles,
                wins=wins,
            )

        self.stdout.write('Создание модулей...')
        modules_data = [
            ('IS-7', 'Двигатель В-12', 'Engine'),
            ('IS-7', 'Орудие С-70', 'Gun'),
            ('E 100', 'Двигатель Maybach HL 230', 'Engine'),
            ('E 100', 'Орудие 12,8 cm Kw.K. 44 L/55', 'Gun'),
            ('T-54 first prototype', 'Орудие Д-10Т', 'Gun'),
            ('Leopard 1', 'Орудие L7A1', 'Gun'),
            ('AMX 13 90', 'Двигатель SOFAM', 'Engine'),
            ('Object 268', 'Орудие М-64', 'Gun'),
        ]
        for tank_name, mod_name, mod_type in modules_data:
            Module.objects.create(
                tank=tanks[tank_name], name=mod_name, module_type=mod_type
            )

        self.stdout.write('Создание боёв...')
        battles_data = [
            ('Sniper_1945', 'IS-7', 3200, True),
            ('Sniper_1945', 'Object 268', 2750, True),
            ('TigerAce', 'E 100', 2900, False),
            ('TigerAce', 'Leopard 1', 1800, True),
            ('LibertyBell', 'M103', 2100, True),
            ('LibertyBell', 'Patton', 1500, False),
            ('ReklessRomeo', 'T-54 first prototype', 950, True),
            ('ReklessRomeo', 'AMX 13 90', 600, False),
            ('Noob228', 'T2 Light Tank', 120, False),
            ('Noob228', 'G.W. Panther', 800, True),
        ]
        for nick, tank_name, damage, victory in battles_data:
            Battle.objects.create(
                player=players[nick],
                tank=tanks[tank_name],
                damage=damage,
                is_victory=victory,
            )

        self.stdout.write(self.style.SUCCESS(
            f'База наполнена: {Tank.objects.count()} танков, '
            f'{Clan.objects.count()} кланов, {Player.objects.count()} игроков, '
            f'{Module.objects.count()} модулей, {Battle.objects.count()} боёв.'
        ))