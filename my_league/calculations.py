from my_league import my_league, transactions


def calculate_team_stats(teams, all_players):
    sorted_team_stats = {}
    for team in teams:
        teams[team][my_league.KEY_STATS] = {}
        team_stats = teams[team][my_league.KEY_STATS]
        for stat in my_league.ALL_STATS:
            team_stats[stat] = 0
        for player in teams[team][my_league.KEY_ROSTER]:
            if player not in all_players or my_league.KEY_IR not in all_players[player]:
                continue # TODO check why this is necessary
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

        for nine_cat_stat in my_league.NINE_CATEGORIES:
            if nine_cat_stat not in sorted_team_stats:
                sorted_team_stats[nine_cat_stat] = []
            stat_list_length = len(sorted_team_stats[nine_cat_stat])
            stat_and_team = [team_stats[nine_cat_stat], team]
            if stat_list_length == 0:
                sorted_team_stats[nine_cat_stat].append(stat_and_team)
            else:
                for index in range(stat_list_length):
                    if team_stats[nine_cat_stat] > sorted_team_stats[nine_cat_stat][index][0]:
                        sorted_team_stats[nine_cat_stat].insert(index, stat_and_team)
                        break
                    elif index + 1 == stat_list_length:
                        sorted_team_stats[nine_cat_stat].append(stat_and_team)
    print(my_league.MY_TEAM + ' stat rankings:')
    for nine_cat_stat in my_league.NINE_CATEGORIES:
        for rank in range(len(teams)):
            if sorted_team_stats[nine_cat_stat][rank][1] == my_league.MY_TEAM:
                print('{} : {}'.format(nine_cat_stat, rank + 1))
                break
            elif rank + 1 == len(teams):
                print('not found: {} {}'.format(my_league.MY_TEAM, nine_cat_stat))


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
