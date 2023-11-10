## ESPN Fantasy Basketball
this repository can be used to simulate the results of an ESPN fantasy basketball regular season

# notes
* projections include all rostered players not in the IR slot, even if they are Out, Suspended, etc.
* match-ups are very rudimentary. category winners are selected as if each player played a single game and produced their statistical average. 

# usage
* replace the my_league.ESPN_LEAGUE_ID with your ESPN League ID
* update my_league.ESPN_STATS_KEY to choose what statistics to use during season simulation
* update my_league.LOAD_FROM_CACHE to choose between using previously cached data or reload
* update my_league.YEAR to the value representing the current season
* execute `main.py` to simulate the season - the output is a `.csv` in the root folder

# set-up
1. using PyCharm, changed interpreter to `pipenv` by clicking the "current interpreter" menu/indicator in the bottom-right
2. installed [espn_api](https://pypi.org/project/espn-api/) with `pipenv install espn_api`

# references:

[style](https://peps.python.org/pep-0008)

