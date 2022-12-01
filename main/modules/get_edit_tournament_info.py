from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect

from main.forms import AddDateTimeMatch
from main.models import *
from main.modules.create_table import get_sort_tables, create_playoff_grid
from main.modules.create_tournament import create_clubs_and_schedule
from main.modules.generate_uid import generate


def get_page_and_context(response, uid):
    tournament = get_tournament_object(uid)

    clubs = Clubs.objects.filter(tournament=tournament.id)
    matches = Matches.objects.filter(tournament=tournament.id)
    completed_matches = matches.filter(status=True)
    uncompleted_matches = matches.filter(status=False)
    access = get_access_level(tournament, response.user)
    best_strikers, disqualified = get_strikers_and_disqualified_players(clubs)
    form_date = AddDateTimeMatch()

    context = {"uid": uid, "tournament": tournament.name, "access": access,
               "clubs": clubs, "completed_matches": completed_matches, "uncompleted_matches": uncompleted_matches,
               "disqualified": disqualified, "goals": best_strikers, "form": form_date}

    if tournament.type == "P":
        playoff_stages = Playoff_scheme.objects.filter(tournament=tournament.id)
        grid = create_playoff_grid(playoff_stages)
        html_file = "main/view_playoff.html"

        context["stages"] = grid

    else:
        table = Tables.objects.filter(tournament=tournament.id).select_related('club')
        table = get_sort_tables(table, tournament.distribution_rules)
        html_file = "main/view_tournament.html"

        context["rows"] = table

        if access == 2:
            league_finished = False if len(uncompleted_matches) else True
            numbers_clubs_to_playoff = [(f"{i}", i) for i in range(3, tournament.count_clubs + 1)]
            context.update({"league_finish": league_finished,
                            "playoff_clubs": numbers_clubs_to_playoff, })

    return html_file, context


def edit_tournament(response, uid):
    tournament = get_tournament_object(uid)
    access_status = get_access_level(tournament, response.user)

    if access_status == 2:
        if response.POST.get("delete-trn"):
            tournament.delete()
            return HttpResponseRedirect("/view/")

        elif response.POST.get("go-to-playoff"):
            tournament_playoff = create_playoff_after_league(response, tournament)
            return HttpResponseRedirect("/tournament/%s" % tournament_playoff.uid)

    if response.POST.get("save-dates") and access_status != 0:
        save_dates(response, tournament)
        return HttpResponseRedirect("")


def create_playoff_after_league(response, tournament):
    clubs_to_po = int(response.POST.get("count-club-to-playoff"))
    rounds = int(response.POST.get("rounds"))
    table = Tables.objects.filter(tournament=tournament.id).select_related('club')
    table = get_sort_tables(table, tournament.distribution_rules)
    table = table[:clubs_to_po]

    tournament_playoff = Tournament(name=(tournament.name + "_playoff"), type="P", count_clubs=clubs_to_po,
                                    rounds=rounds, cards=tournament.cards)

    tournament_playoff.save()
    tournament_playoff.uid = generate()
    tournament_playoff.save(update_fields=['uid'])

    response.user.tournament.add(tournament_playoff)

    clubs_playoff = []
    for i in table:
        clubs_playoff.append(i[1])

    create_clubs_and_schedule(clubs_playoff, tournament_playoff, False)

    list_players = []

    for i in table:
        players = Players.objects.filter(club=i[0])
        new_club = Clubs.objects.filter(tournament=tournament_playoff).get(name=i[1])

        for player in players:
            player.pk = None
            player.club = new_club
            list_players.append(player)

    Players.objects.bulk_create(list_players)

    return tournament_playoff


def save_dates(response, tournament):
    matches = Matches.objects.filter(tournament=tournament.id)
    matchday = response.POST.dict()
    match_upd = matches.filter(status=False)

    for match in match_upd:
        if matchday[f"{match.id}"]:
            match.matchday = matchday[f"{match.id}"]

    Matches.objects.bulk_update(match_upd, ["matchday"])


def get_tournament_object(uid):
    try:
        tournament = Tournament.objects.get(uid=uid)
        return tournament
    except ObjectDoesNotExist:
        raise Http404


# 0 - user, 1 - admin, 2 - owner
def get_access_level(tournament, user):
    if tournament.owner == user:
        return 2
    elif tournament.admins.filter(username=user.username):
        return 1
    else:
        return 0


def get_strikers_and_disqualified_players(clubs):
    best_strikers = []
    disqualified = []

    for club in clubs:
        players = Players.objects.filter(club=club)

        for player in players:
            if player.disqualified: disqualified.append((player.club, player.number, player.name))
            if player.goals > 0: best_strikers.append((player.club, player.number, player.name, player.goals))

    best_strikers = sorted(best_strikers, key=lambda player: player[3], reverse=True)

    return best_strikers, disqualified
