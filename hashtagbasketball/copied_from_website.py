import csv


def get_stats():
    all_player_stats_map = {}
    # copied.csv created from copying the table from hashtagbasketball and pasting into a UTF8 spreadsheet
    # and players names have been updated to match ESPN, where necessary
    with open('hashtagbasketball/copied.csv', 'r', newline='\n', encoding='utf8') as stats_file:
        reader = csv.DictReader(stats_file)
        for row in reader:
            if row['R#'] == 'R#':
                continue
            player_name = to_espn_name(row['PLAYER'])
            [fgm, fga] = percent_to_made_and_total(row['FG%'])
            [ftm, fta] = percent_to_made_and_total(row['FT%'])
            all_player_stats_map[player_name] = {
                'FGM': float(fgm),
                'FGA': float(fga),
                'FTM': float(ftm),
                'FTA': float(fta),
                '3PTM': float(row['3PM']),
                'REB': float(row['TREB']),
                'AST': float(row['AST']),
                'STL': float(row['STL']),
                'BLK': float(row['BLK']),
                'PTS': float(row['PTS']),
                'TO' : float(row['TO'])
            }
    return all_player_stats_map


# assumption: percent is in the format `FG% (FGM/FGA)`, example: `0.624 (9.9/15.9)`
def percent_to_made_and_total(percent):
    made_and_attemped = percent.split(' ')
    [made, attempted] = made_and_attemped[1].split('/')
    made = made[1:]
    attempted = attempted[:len(attempted) - 1]
    return [float(made), float(attempted)]


def to_espn_name(hashtag_name):
    if hashtag_name == 'OG Anunoby':
        return "O.G. Anunoby"
    elif hashtag_name == 'Nicolas Claxton':
        return 'Nic Claxton'
    elif hashtag_name == 'Alperen Sengn' or hashtag_name == 'Alperen Sengün':
        return 'Alperen Sengun'
    elif hashtag_name == 'Dennis Schr”der' or hashtag_name == 'Dennis Schröder':
        return 'Dennis Schroder'
    elif hashtag_name == 'Xavier Tillman Sr.':
        return 'Xavier Tillman'
    elif hashtag_name == 'Reggie Bullock':
        return 'Reggie Bullock Jr.'
    elif hashtag_name == 'Aleksandar Vezenkov':
        return 'Sasha Vezenkov'
    elif hashtag_name == 'Th‚o Maledon' or hashtag_name == 'Théo Maledon':
        return 'Theo Maledon'
    elif hashtag_name == '™mer Yurtseven' or hashtag_name == 'Ömer Yurtseven':
        return 'Omer Yurtseven'
    elif hashtag_name == 'Patrick Baldwin Jr.':
        return 'Patrick Baldwin'
    elif hashtag_name == 'Andre Jackson':
        return 'Andre Jackson Jr.'
    elif hashtag_name == 'EJ Liddell':
        return 'E.J. Liddell'
    return hashtag_name
