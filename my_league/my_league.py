from saving_and_caching import caches
from espn_interactions import league_interactions
from my_league import calculations
from my_league import results

ESPN_LEAGUE_ID = 1192749948
YEAR = 2024  # 2024 is 2023-2024 season
ALL_STATS = ['FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
NINE_CATEGORIES = ['FG%', 'FT%', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
KEY_IR = 'On IR'
KEY_ROSTER = 'roster'
KEY_STATS = 'stats'
KEY_WINS = 'wins'
KEY_LOSSES = 'losses'
KEY_TIES = 'ties'
LOAD_FROM_CACHE = True


def process():
    if LOAD_FROM_CACHE:
        all_players_stat_map = caches.get_players()
        teams = caches.get_teams()
        schedule = caches.get_schedule()
    else:
        espn_league = league_interactions.get_league_from_espn(ESPN_LEAGUE_ID, YEAR)
        all_players_stat_map = league_interactions.construct_players_stat_map(espn_league)
        teams = league_interactions.extract_rosters_from_espn_league(espn_league)
        schedule = league_interactions.extract_schedules_from_espn_league(espn_league)
        caches.cache_league_objects(teams, all_players_stat_map, schedule)

    combine_team_info(teams, schedule)

    calculations.calculate_team_stats(teams, all_players_stat_map)
    calculations.simulate_season(teams)

    results.stats_and_results_to_csv(teams)

    print('processing complete')


def combine_team_info(teams, schedule):
    for team_name in teams:
        teams[team_name] = {KEY_ROSTER: teams[team_name]}
        teams[team_name]['schedule'] = schedule[team_name]
