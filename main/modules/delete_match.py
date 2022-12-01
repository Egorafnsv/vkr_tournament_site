from ..models import Tables, Players
from django.db import models


def delete_match(match):
    home_record = Tables.objects.get(club=match.club_home)
    away_record = Tables.objects.get(club=match.club_away)

    home_goals = match.home_goals
    away_goals = match.away_goals

    if home_goals > away_goals:
        home_record.win = models.F("win") - 1
        away_record.lose = models.F("lose") - 1
    elif home_goals < away_goals:
        home_record.lose = models.F("lose") - 1
        away_record.win = models.F("win") - 1
    else:
        home_record.draw = models.F("draw") - 1
        away_record.draw = models.F("draw") - 1

    home_record.goals_for = models.F("goals_for") - home_goals
    home_record.goals_against = models.F("goals_against") - away_goals
    away_record.goals_for = models.F("goals_for") - away_goals
    away_record.goals_against = models.F("goals_against") - home_goals

    # actions field: "yellows:red:goals_home:goals_away" ---inside---> "player_id,player_id,:player_id,player_id,:"
    match_actions = match.actions.split(":")

    if len(match_actions[0]) > 1:
        for i in match_actions[0].split(",")[:-1]:  # yellow cards
            player = Players.objects.get(id=i)
            player.yellow = models.F("yellow") - 1
            player.save()

    if len(match_actions[1]) > 1:
        for i in match_actions[1].split(",")[:-1]:  # red cards
            player = Players.objects.get(id=i)
            player.red = models.F("red") - 1
            player.save()

    if len(match_actions[2]) > 1:
        for i in match_actions[2].split(",")[:-1]:  # goals home
            player = Players.objects.get(id=i)
            player.goals = models.F("goals") - 1
            player.save()

    if len(match_actions[3]) > 1:
        for i in match_actions[3].split(",")[:-1]:  # goals away
            player = Players.objects.get(id=i)
            player.goals = models.F("goals") - 1
            player.save()

    match.home_goals = 0
    match.away_goals = 0
    match.status = False
    match.actions = None
    match.save()
    home_record.save()
    away_record.save()
