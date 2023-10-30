import csv
import os
from my_league import my_league

HEADER_PLAYER = 'Player'


def get_path_cache():
    return 'cached/{}'.format(my_league.ESPN_LEAGUE_ID)


def get_players():
    all_players = {}
    with open('{}/players.csv'.format(get_path_cache()), 'r', newline='\n') as players_file:
        reader = csv.DictReader(players_file)
        for row in reader:
            all_players[row[HEADER_PLAYER]] = {}
            for stat in my_league.ALL_STATS:
                all_players[row[HEADER_PLAYER]][stat] = int(float(row[stat]))
            all_players[row[HEADER_PLAYER]][my_league.KEY_IR] = row[my_league.KEY_IR]
    return all_players


def get_teams():
    teams = {}
    for (__, __, filenames) in os.walk('./{}/teams/'.format(get_path_cache())):
        for file in filenames:
            team_name = file[0:-4]
            teams[team_name] = []
            with open('{}/teams/'.format(get_path_cache()) + file, 'r', newline='\r\n') as team_file:
                for line in team_file:
                    teams[team_name] += [line.rstrip('\r\n')]
    return teams


def get_schedule():
    schedules = {}
    for (__, __, filenames) in os.walk('./{}/schedules/'.format(get_path_cache())):
        for file in filenames:
            team_name = file[0:-4]
            schedules[team_name] = []
            with open('{}/schedules/'.format(get_path_cache()) + file, 'r', newline='\r\n') as team_schedule:
                for line in team_schedule:
                    schedules[team_name] += [line.rstrip('\r\n')]
    return schedules


def init_cache_folders():
    if not os.path.exists('cached'):
        os.makedirs('cached')
    if not os.path.exists(get_path_cache()):
        os.makedirs(get_path_cache())
    # TODO: need to clear existing teams and schedule cache first.
    # example: when teams are different from last year
    if not os.path.exists(get_path_cache() + '/teams'):
        os.makedirs(get_path_cache() + '/teams')
    if not os.path.exists(get_path_cache() + '/schedules'):
        os.makedirs(get_path_cache() + '/schedules')


def cache_league_objects(teams, players, schedule):
    init_cache_folders()
    for name in teams:
        safe_name = name.replace('?', '')
        with open('{}/teams/{}.csv'.format(get_path_cache(), safe_name), 'w', newline='\n') as team_file:
            for player in teams[name]:
                writer = csv.writer(team_file)
                writer.writerow([player])
    for team_name in schedule:
        safe_name = team_name.replace('?', '')
        with open('{}/schedules/{}.csv'.format(get_path_cache(), safe_name), 'w', newline='\n') as schedule_file:
            for matchup in schedule[team_name]:
                writer = csv.writer(schedule_file)
                writer.writerow([matchup])
    with open('{}/players.csv'.format(get_path_cache()), 'w', newline='\n') as players_file:
        writer = csv.DictWriter(players_file, fieldnames=[HEADER_PLAYER] + my_league.ALL_STATS + [my_league.KEY_IR])
        writer.writeheader()
        for name in players:
            players[name][HEADER_PLAYER] = name
            writer.writerow(players[name])
