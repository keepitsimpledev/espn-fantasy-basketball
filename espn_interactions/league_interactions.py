from espn_api.basketball import League, Team, Matchup
from my_league import my_league


def get_league_from_espn(league_id, year):
    return League(league_id, year)


def extract_schedules_from_espn_league(league: League):
    schedules = {}
    for team in league.teams:
        team_name = get_formatted_name_from_espn_team_object(team)
        schedules[team_name] = []
        week: Matchup
        for week in team.schedule:
            home_team_name = get_formatted_name_from_espn_team_object(week.home_team)
            away_team_name = get_formatted_name_from_espn_team_object(week.away_team)
            opponent = home_team_name if team_name == away_team_name else away_team_name
            schedules[team_name] += [opponent.replace('?', '').replace('⭐', '')]
    return schedules


def extract_rosters_from_espn_league(league: League):
    teams = {}
    for team in league.teams:
        name = get_formatted_name_from_espn_team_object(team)
        players = []
        for player in team.roster:
            players += [player.name]
        teams[name] = players
    return teams


def extract_all_players_from_espn_league(league: League):
    all_players = []
    for team in league.teams:
        all_players += team.roster
    free_agents = league.free_agents(size=1000)
    all_players += free_agents
    return all_players


def construct_players_stat_map(league: League):
    all_espn_player_objects = extract_all_players_from_espn_league(league)
    all_players_stat_map = {}
    for player in all_espn_player_objects:
        all_players_stat_map[player.name] = {}
        projections_not_found = []
        for stat in my_league.ALL_STATS:
            if my_league.ESPN_STATS_KEY in player.stats \
                    and 'total' in player.stats[my_league.ESPN_STATS_KEY] \
                    and stat in player.stats[my_league.ESPN_STATS_KEY]['total']:
                value = player.stats[my_league.ESPN_STATS_KEY]['total'][stat]
                all_players_stat_map[player.name][stat] = int(value)
            else:
                # previously we used previous year's average, but that seems to now be unavailable in the ESPN API
                projections_not_found.append(stat)
                all_players_stat_map[player.name][stat] = 0
        all_players_stat_map[player.name][my_league.KEY_IR] = player.lineupSlot == 'IR'
        if len(projections_not_found) > 0:
            print('{} projections not found: {}'.format(player.name, ', '.join(projections_not_found)))
    return all_players_stat_map


def get_formatted_name_from_espn_team_object(espn_team: Team):
    return '{} ({})'.format(espn_team.team_name, espn_team.team_abbrev).replace('?', '').replace('⭐', '')
