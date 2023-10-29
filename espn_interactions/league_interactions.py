from espn_api.basketball import League
from my_league import my_league

PROJECTIONS_KEY = '2024_projected'


def get_league_from_espn(league_id, year):
    return League(league_id, year)


def extract_all_players_from_espn_league(league):
    all_players = []
    for team in league.teams:
        all_players += team.roster
    free_agents = league.free_agents(size=500)
    all_players += free_agents
    return all_players


def construct_players_stat_map(league):
    all_espn_player_objects = extract_all_players_from_espn_league(league)
    all_players_stat_map = {}
    for player in all_espn_player_objects:
        all_players_stat_map[player.name] = {}
        projections_not_found = []
        for stat in my_league.ALL_STATS:
            if PROJECTIONS_KEY in player.stats and 'total' in player.stats[PROJECTIONS_KEY] and stat in player.stats[PROJECTIONS_KEY]['total']:
                value = player.stats[PROJECTIONS_KEY]['total'][stat]
                all_players_stat_map[player.name][stat] = float(value)
            else:
                # previously we used previous year's average, but that seems to now be unavailable in the ESPN API
                projections_not_found.append(stat)
                all_players_stat_map[player.name][stat] = 0
        all_players_stat_map[player.name][my_league.IR_KEY] = player.lineupSlot == 'IR'
        if len(projections_not_found) > 0:
            print('{} projections not found: {}'.format(player.name, ', '.join(projections_not_found)))
    return all_players_stat_map
