import csv
import os
from my_league import my_league

HEADER_PLAYER = 'Player'


def get_path_cache():
    return 'cached/{}'.format(my_league.BJSS_LEAGUE_ID)


def get_league():
    return "this is a league"


def get_players():
    all_players = {}
    with open('{}/players.csv'.format(get_path_cache()), 'r', newline='\n') as players_file:
        reader = csv.DictReader(players_file)
        for row in reader:
            all_players[row[HEADER_PLAYER]] = {}
            for stat in my_league.ALL_STATS:
                all_players[row[HEADER_PLAYER]][stat] = int(float(row[stat]))
            all_players[row[HEADER_PLAYER]][my_league.IR_KEY] = row[my_league.IR_KEY]
    return all_players


def get_teams():
    bjss_teams = {}
    for (__, __, filenames) in os.walk('./{}/teams/'.format(get_path_cache())):
        for file in filenames:
            team_name = file[0:-4]
            bjss_teams[team_name] = []
            with open('{}/teams/'.format(get_path_cache()) + file, 'r', newline='\r\n') as team_file:
                for line in team_file:
                    bjss_teams[team_name] += [line.rstrip('\r\n')]
    return bjss_teams


def create_cache_folders_if_necessary():
    if not os.path.exists('cached'):
        os.makedirs('cached')
    if not os.path.exists(get_path_cache()):
        os.makedirs(get_path_cache())
    if not os.path.exists(get_path_cache() + '/teams'):
        os.makedirs(get_path_cache() + '/teams')


# def cache_league_objects(teams, players, schedule):
def cache_league_objects(teams, players):
    create_cache_folders_if_necessary()
    # TODO: need to clear existing cache first. example: when teams are different from last year
    # TODO: create folders if they do not yet exist
    for name in teams:
        safe_name = name.replace('?', '')
        with open('{}/teams/{}.csv'.format(get_path_cache(), safe_name), 'w', newline='\n') as team_file:
            for player in teams[name]:
                writer = csv.writer(team_file)
                writer.writerow([player])
    # for team_name in schedule:
    #     safe_name = team_name.replace('?', '')
    #     with open('{}/schedules/{}.csv'.format(__cache_folder, safe_name), 'w', newline='\n') as schedule_file:
    #         for matchup in schedule[team_name]:
    #             writer = csv.writer(schedule_file)
    #             writer.writerow([matchup])
    with open('{}/players.csv'.format(get_path_cache()), 'w', newline='\n') as players_file:
        writer = csv.DictWriter(players_file, fieldnames=[HEADER_PLAYER] + my_league.ALL_STATS + [my_league.IR_KEY])
        writer.writeheader()
        for name in players:
            players[name][HEADER_PLAYER] = name
            writer.writerow(players[name])
