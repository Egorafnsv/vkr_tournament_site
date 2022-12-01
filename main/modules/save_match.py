from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect

from main.models import Tables, Playoff_scheme, Matches, Players
from django.db.models import F

from main.modules.check_next_stage import check_next_stage
from main.modules.get_edit_tournament_info import get_access_level


def get_context_add_page(match, user, tournament_uid):
    if match.tournament.uid != tournament_uid:
        raise Http404("Такой страницы не существует!")
    elif get_access_level(match.tournament, user) == 0:
        raise PermissionDenied

    home_players = Players.objects.filter(club=match.club_home.id)
    away_players = Players.objects.filter(club=match.club_away.id)

    context = {"match": match, "home_players": home_players, "away_players": away_players, }

    if match.tournament.type == "P":
        stage = match.playoff_stage.id
        matches = Matches.objects.filter(playoff_stage=stage).filter(status=False).values_list("serial_number",
                                                                                               flat=True)
        matches = list(matches)
        matches.sort()

        last_match_in_stage = match.serial_number == matches[-1]
        last_match_left = len(matches) == 1
        score = []
        if last_match_left:
            score.append(Playoff_scheme.objects.get(id=stage).home_goals)
            score.append(Playoff_scheme.objects.get(id=stage).away_goals)
            context.update({"last_match": last_match_left, "total_score": score})
        else:
            context.update({"last_match_in_stage": last_match_in_stage, "total_score": score, })

    return context


def save_match(home_players_goals, away_players_goals, context_match, home_goals, away_goals, yellows, reds, deleted_from_disqualified):
    save_result(context_match["match"], home_goals, away_goals)
    save_statistics(home_players_goals, away_players_goals, context_match, yellows, reds, deleted_from_disqualified)


# если тип playoff, проверяет на переход в следующую стадию и осуществляет его
def save_result(match, home_goals, away_goals):
    match.home_goals = home_goals
    match.away_goals = away_goals
    match.status = True
    match.save()

    if match.tournament.type != "P":
        home_record = Tables.objects.get(club=match.club_home)
        away_record = Tables.objects.get(club=match.club_away)

        if home_goals > away_goals:
            home_record.win = F("win") + 1
            away_record.lose = F("lose") + 1

        elif home_goals < away_goals:
            home_record.lose = F("lose") + 1
            away_record.win = F("win") + 1

        else:
            home_record.draw = F("draw") + 1
            away_record.draw = F("draw") + 1

        home_record.goals_for = F("goals_for") + home_goals
        home_record.goals_against = F("goals_against") + away_goals

        away_record.goals_for = F("goals_for") + away_goals
        away_record.goals_against = F("goals_against") + home_goals

        home_record.save()
        away_record.save()

    else:
        stage = match.playoff_stage.id
        match_playoff = Playoff_scheme.objects.get(id=stage)
        match_playoff.home_goals = F("home_goals") + home_goals
        match_playoff.away_goals = F("away_goals") + away_goals
        match_playoff.save()

        if match_playoff.stage != "1_0":
            check_next_stage(Playoff_scheme.objects.get(id=stage))


def save_statistics(home_players_goals, away_players_goals, context_match, yellows, reds, deleted_from_disqualified):
    actions = ""
    limit_yellow = context_match["match"].tournament.cards

    players_update_list = []

    for i in deleted_from_disqualified:
        player = Players.objects.get(id=i)
        player.disqualified = False
        players_update_list.append(player)

    Players.objects.bulk_update(players_update_list, ["disqualified"])

    players_update_list = []

    for player_id in yellows:
        player = Players.objects.get(id=player_id)
        player.yellow += 1
        if player.yellow % limit_yellow == 0:
            player.disqualified = True
        players_update_list.append(player)
        actions += (str(player.id) + ",")

    actions += ":"

    for player_id in reds:
        player = Players.objects.get(id=player_id)
        player.red = F("red") + 1
        player.disqualified = True
        players_update_list.append(player)
        actions += (str(player.id) + ",")

    Players.objects.bulk_update(players_update_list, ["yellow", "red", "disqualified"])

    actions += ":"

    players_update_list = []

    for player_id in home_players_goals:
        goals = home_players_goals[player_id]
        player = context_match["home_players"].get(id=player_id.split("_")[-1])

        if goals != "0":
            goals = int(goals)
            player.goals = F("goals") + goals

            actions += ((str(player.id) + ",") * goals)

        players_update_list.append(player)

    actions += ":"

    for player_id in away_players_goals:
        goals = away_players_goals[player_id]
        player = context_match["away_players"].get(id=player_id.split("_")[-1])

        if goals != "0":
            goals = int(goals)
            player.goals = F("goals") + goals

            actions += ((str(player.id) + ",") * goals)

        players_update_list.append(player)

    Players.objects.bulk_update(players_update_list, ["goals"])

    context_match["match"].actions = actions

    context_match["match"].save()
