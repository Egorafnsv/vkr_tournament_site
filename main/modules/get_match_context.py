from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from main.models import Matches, Players
from main.modules.get_edit_tournament_info import get_access_level


def get_match_context(user, uid, match_id):
    match = Matches.objects.get(id=match_id)
    tournament = match.tournament

    if tournament.uid != uid:
        raise Http404

    access = get_access_level(tournament, user) != 0

    # 'actions' field: "yellows:red:goals_home:goals_away" ---inside---> "player_id,player_id,:player_id,player_id,:"
    match_actions = match.actions.split(":")

    home_yellow_cards = []
    home_red_cards = []
    home_goals = []

    away_yellow_cards = []
    away_red_cards = []
    away_goals = []

    if len(match_actions[0]) > 1:
        for i in match_actions[0].split(",")[:-1]:  # yellow cards
            try:
                player = Players.objects.get(id=i)

                if player.club.id == match.club_home.id:
                    home_yellow_cards.append([player.number, player.name])
                else:
                    away_yellow_cards.append([player.number, player.name])
            except ObjectDoesNotExist:
                continue

    if len(match_actions[1]) > 1:
        for i in match_actions[1].split(",")[:-1]:  # red cards
            try:
                player = Players.objects.get(id=i)
                if player.club.id == match.club_home.id:
                    home_red_cards.append((player.number, player.name))
                else:
                    away_red_cards.append((player.number, player.name))
            except ObjectDoesNotExist:
                continue

    if len(match_actions[2]) > 1:
        for i in match_actions[2].split(",")[:-1]:  # home goals
            try:
                player = Players.objects.get(id=i)
                home_goals.append((player.number, player.name))
            except ObjectDoesNotExist:
                home_goals.append(("0", "Игрок был удален"))

    if len(match_actions[3]) > 1:
        for i in match_actions[3].split(",")[:-1]:  # away goals
            try:
                player = Players.objects.get(id=i)
                away_goals.append((player.number, player.name))
            except ObjectDoesNotExist:
                away_goals.append(("0", "Игрок был удален"))

    return {"match": match, "access": access, "home_yellow": home_yellow_cards, "home_red": home_red_cards,
                                              "home_goals": home_goals,
                                              "away_yellow": away_yellow_cards, "away_red": away_red_cards,
                                              "away_goals": away_goals}
