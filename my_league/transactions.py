from my_league import my_league


# example usage: drop('Daniel Theis', teams)
def drop(player, teams):
    for team_name in teams:
        roster = teams[team_name][my_league.KEY_ROSTER]
        if player in roster:
            del roster[roster.index(player)]
            return team_name
    print('unable to drop {} - not found'.format(player))


# example usage: add('Luke Kennard', 'Flint Tropics (ELE)', all_players, teams)
def add(player, team, all_players, all_teams):
    if player not in all_players:
        print('unable to add {} - player not found'.format(player))
    elif team not in all_teams:
        print('unable to add to {} - team not found'.format(team))
    else:
        all_teams[team][my_league.KEY_ROSTER] += [player]


# example usage, 1-for-1 trade: trade(['Mason Plumlee'], ['Robert Covington'], bjss_teams)
# example usage, 3-for-3 trade: trade(['Mason Plumlee', 'Davis Bertans', 'Kyrie Irving'],
#                                   ['Dejounte Murray', 'Markelle Fultz', 'Robert Covington'], bjss_teams)
def trade(player_set_1, player_set_2, teams):
    players1_ex = []
    for player in player_set_1:
        players1_ex += [drop(player, teams)]
    assert len(player_set_1) == len(players1_ex)
    for i in range(len(players1_ex) - 1):
        assert players1_ex[i] == players1_ex[i + 1], 'cross-team trade'
    players1_ex = players1_ex[0]

    players2_ex = []
    for player in player_set_2:
        players2_ex += [drop(player, teams)]
    assert len(player_set_2) == len(players2_ex)
    for i in range(len(players2_ex) - 1):
        assert players2_ex[i] == players2_ex[i + 1], 'cross-team trade'
    players2_ex = players2_ex[0]

    for player in player_set_1:
        teams[players2_ex][my_league.KEY_ROSTER] += [player]
    for player in player_set_2:
        teams[players1_ex][my_league.KEY_ROSTER] += [player]
