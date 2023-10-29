import csv
import os
from my_league import my_league

PATH_CACHE = r'cached'
HEADER_PLAYER = 'Player'


def get_league():
    create_cache_folders_if_necessary()
    return "this is a league"


def create_cache_folders_if_necessary():
    if not os.path.exists(PATH_CACHE):
        os.makedirs(PATH_CACHE)


# def cache_league_objects(teams, players, schedule):
def cache_league_objects(players):
    # TODO: need to clear existing cache first. example: when teams are different from last year
    # TODO: create folders if they do not yet exist
    # for name in teams:
    #     safe_name = name.replace('?', '')
    #     with open('{}/teams/{}.csv'.format(__cache_folder, safe_name), 'w', newline='\n') as team_file:
    #         for player in teams[name]:
    #             writer = csv.writer(team_file)
    #             writer.writerow([player])
    # for team_name in schedule:
    #     safe_name = team_name.replace('?', '')
    #     with open('{}/schedules/{}.csv'.format(__cache_folder, safe_name), 'w', newline='\n') as schedule_file:
    #         for matchup in schedule[team_name]:
    #             writer = csv.writer(schedule_file)
    #             writer.writerow([matchup])
    with open('{}/players.csv'.format(PATH_CACHE), 'w', newline='\n') as players_file:
        writer = csv.DictWriter(players_file, fieldnames=[HEADER_PLAYER] + my_league.ALL_STATS + [my_league.IR_KEY])
        writer.writeheader()
        for name in players:
            players[name][HEADER_PLAYER] = name
            writer.writerow(players[name])
