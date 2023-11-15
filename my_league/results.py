import csv
from my_league import my_league


def stats_and_results_to_csv(teams):
    with open('fantasy nba projection (league {} year {}).csv'.format(my_league.ESPN_LEAGUE_ID, my_league.YEAR), 'w', newline='\n') as file:
        headers = ['Team Name'] + ['Standing'] + my_league.NINE_CATEGORIES + ['Record']
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        teams = sort_by_record(to_array(teams))
        rank = 1
        for name_and_data in teams:
            team = name_and_data[1]
            entry = name_and_data[1][my_league.KEY_STATS]
            entry['Team Name'] = name_and_data[0]
            entry['Record'] = '{}-{}-{}'.format(team[my_league.KEY_WINS], team[my_league.KEY_LOSSES], team[my_league.KEY_TIES])
            entry['Standing'] = rank
            writer.writerow(entry)
            if entry['Team Name'] == my_league.MY_TEAM:
                print('{} projected rank: {} record: {}'.format(entry['Team Name'], rank, entry['Record']))
            rank += 1


def sort_by_record(teams_list):
    if len(teams_list) <= 1:
        return teams_list
    elif len(teams_list) == 2:
        if compare(teams_list[0], teams_list[1]) == -1:
            return [teams_list[0], teams_list[1]]
        else:
            return [teams_list[1], teams_list[0]]
    else:
        left = teams_list[0:int(len(teams_list)/2)]
        left = sort_by_record(left)
        right = teams_list[int(len(teams_list)/2):len(teams_list)]
        right = sort_by_record(right)
        left_index = 0
        right_index = 0
        ordered_teams = []
        while left_index < len(left) or right_index < len(right):
            if left_index == len(left):
                ordered_teams.append(right[right_index])
                right_index += 1
            elif right_index == len(right):
                ordered_teams.append(left[left_index])
                left_index += 1
            elif compare(left[left_index], right[right_index]) == -1:
                ordered_teams.append(left[left_index])
                left_index += 1
            else:
                ordered_teams.append(right[right_index])
                right_index += 1
        return ordered_teams


def compare(team_a, team_b):
    if team_a[1][my_league.KEY_WINS] > team_b[1][my_league.KEY_WINS] or team_a[1][my_league.KEY_LOSSES] < team_b[1][my_league.KEY_LOSSES]:
        return -1
    else:
        return 1


def to_array(teams):
    teams_list = []
    for team in teams:
        teams_list.append([team, teams[team]])
    return teams_list
