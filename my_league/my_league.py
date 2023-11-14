from saving_and_caching import caches
from espn_interactions import league_interactions
from hashtagbasketball import copied_from_website
from my_league import calculations, results, transactions

BJSS_LEAGUE_ID = 1192749948
BJSS_LEAGUE_TEAM = 'Flint Tropics (ELE)'
TASD_LEAGUE_ID = 917926052
TASD_LEAGUE_TEAM = 'Timo Cruz (TIMO)'

# replace with your ESPN league ID:
ESPN_LEAGUE_ID = TASD_LEAGUE_ID
MY_TEAM = TASD_LEAGUE_TEAM

# TODO: cache projects, total, and last 7, and change filename
ESPN_PROJECTIONS_KEY = '2024_projected'
ESPN_TOTAL_KEY = '2024_total'
ESPN_LAST_7_KEY = '2024_last_7'
ESPN_STATS_KEY = ESPN_PROJECTIONS_KEY
USE_HASHTAG = True

LOAD_FROM_CACHE = False

YEAR = 2024  # 2024 is 2023-2024 season


ALL_STATS = ['FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
NINE_CATEGORIES = ['FG%', 'FT%', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
KEY_IR = 'On IR'
KEY_ROSTER = 'roster'
KEY_STATS = 'stats'
KEY_WINS = 'wins'
KEY_LOSSES = 'losses'
KEY_TIES = 'ties'


def process():
    [teams, all_players_stat_map] = load()

    process_transactions(teams, all_players_stat_map)

    calculations.calculate_team_stats(teams, all_players_stat_map)
    calculations.simulate_season(teams)

    # calculations.find_fa_upgrades(teams, all_players_stat_map)

    results.stats_and_results_to_csv(teams)

    print('processing complete')


def process_transactions(teams, all_players):
    # sample transactions:
    # transactions.drop('Al Horford', teams)
    # transactions.add('Cedi Osman', 'Flint Tropics (ELE)', all_players, teams)
    # transactions.trade(['Nikola Jokic'],
    #                    ['Joel Embiid'],
    #                    teams)
    # TODO: add check to confirm no teams have more than 13 players
    print('transactions processed')


def load():
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

    if USE_HASHTAG:
        all_players_stat_map = get_player_stat_map_from_hashtag(all_players_stat_map)

    combine_team_info(teams, schedule)

    return [teams, all_players_stat_map]


def combine_team_info(teams, schedule):
    for team_name in teams:
        teams[team_name] = {KEY_ROSTER: teams[team_name]}
        teams[team_name]['schedule'] = schedule[team_name]


def get_player_stat_map_from_hashtag(all_players_stat_map):
    hashtag_players_stat_map = copied_from_website.get_stats()
    for hashtag_player in hashtag_players_stat_map:
        if hashtag_player in all_players_stat_map:
            hashtag_players_stat_map[hashtag_player][KEY_IR] = all_players_stat_map[hashtag_player][KEY_IR]
        else:
            print('player not found in ESPN: ' + hashtag_player)
    return hashtag_players_stat_map
