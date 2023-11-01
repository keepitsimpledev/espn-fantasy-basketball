from my_league import my_league


def calculate_team_stats(teams, all_players):
    for team in teams:
        teams[team][my_league.KEY_STATS] = {}
        team_stats = teams[team][my_league.KEY_STATS]
        for stat in my_league.ALL_STATS:
            team_stats[stat] = 0
        for player in teams[team][my_league.KEY_ROSTER]:
            if all_players[player][my_league.KEY_IR] == 'True':
                continue
            for stat in my_league.ALL_STATS:
                team_stats[stat] += all_players[player][stat]
        fg_pct = team_stats['FGM'] / team_stats['FGA']
        ft_pct = team_stats['FTM'] / team_stats['FTA']
        del team_stats['FGM'], team_stats['FGA'], team_stats['FTM'], team_stats['FTA']
        team_stats['FG%'] = round(fg_pct, 4)
        team_stats['FT%'] = round(ft_pct, 4)
        team_stats['TO'] = team_stats['TO'] * -1


def simulate_season(teams):
    for team_name in teams:
        wins = losses = ties = 0
        team_stats = teams[team_name][my_league.KEY_STATS]
        for matchup in teams[team_name]['schedule']:
            opponent_stats = teams[matchup][my_league.KEY_STATS]
            for stat in my_league.NINE_CATEGORIES:
                if team_stats[stat] > opponent_stats[stat]:
                    wins += 1
                elif team_stats[stat] < opponent_stats[stat]:
                    losses += 1
                else:
                    ties += 1
        teams[team_name][my_league.KEY_WINS] = wins
        teams[team_name][my_league.KEY_LOSSES] = losses
        teams[team_name][my_league.KEY_TIES] = ties
