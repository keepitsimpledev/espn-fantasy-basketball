from saving_and_caching import caches
from espn_interactions import league_interactions

BJSS_LEAGUE_ID = 1192749948
YEAR = 2024  # 2024 is 2023-2024 season
ALL_STATS = ['FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
# NINE_CATEGORIES = ['FG%', 'FT%', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
IR_KEY = 'On IR'
USE_CACHE = False


def process():
    if USE_CACHE:
        my_league = caches.get_league()
    else:
        espn_league = league_interactions.get_league_from_espn(BJSS_LEAGUE_ID, YEAR)
        all_players_stat_map = league_interactions.construct_players_stat_map(espn_league)
        caches.cache_league_objects(all_players_stat_map)

    print(caches.get_league())
