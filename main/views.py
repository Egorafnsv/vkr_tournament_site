from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .forms import CreateNewPlayer, CreateNewTournament
from .models import *

from .modules.Club import Club
from .modules.create_tournament import create_tournament
from .modules.get_edit_tournament_info import get_access_level, get_page_and_context
from .modules.delete_match import delete_match
from .modules.get_edit_tournament_info import edit_tournament
from .modules.get_match_context import get_match_context
from .modules.save_match import save_match, get_context_add_page


# Create your views here.

def list_tournaments(response):
    return render(response, "main/list_tournaments.html")


def type_tournament_create(response):
    return render(response, "main/create_tournament.html", {"choose": True})


def create_new_tournament(response, type_tournament):
    if response.method == "POST":
        form = CreateNewTournament(response.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            rounds = form.cleaned_data["rounds"]
            cards = form.cleaned_data["cards"]
            clubs = response.POST.getlist("new-club")
            shuffle = response.POST.get("shuffle")
            rules_raw = {k: v for k, v in response.POST.items() if k.startswith("select_")}

            return create_tournament(response.user, name, type_tournament, clubs, rounds, cards, rules_raw, shuffle)
    else:
        form = CreateNewTournament()

    return render(response, "main/create_tournament.html", {"form": form, "type": type_tournament})


def view_tournament(response, uid):
    path_to_html, context = get_page_and_context(response, uid)

    if response.method == "POST":
        return edit_tournament(response, uid)

    print(path_to_html)
    return render(response, path_to_html, context)


def view_club(response, uid, id):
    club = Club(id)

    if club.club.tournament.uid != uid:
        raise Http404

    access = get_access_level(club.tournament, response.user)

    if response.method == "POST" and access:
        if response.POST.get("add-players"):
            club.add_players(response)

        elif response.POST.get("del-players"):
            club.delete_players(response.POST.getlist("delete-player"))

        elif response.POST.get("add-notes"):
            club.add_notes(response.POST.get("notes"))

    form = CreateNewPlayer(club.get_free_numbers())

    return render(response, "main/view_club.html", {"club": club, "form": form, "access": access})


def add_score(response, tournament_uid, match_id):
    match = Matches.objects.get(id=match_id)
    context_match = get_context_add_page(match, response.user, tournament_uid)

    if response.method == "POST":
        if response.POST.get("save"):
            home_goals = response.POST.get("home_goals")
            away_goals = response.POST.get("away_goals")
            yellows = response.POST.getlist("yellow")
            reds = response.POST.getlist("red")
            deleted_from_disqualified = response.POST.getlist("disq")
            home_players_goals = {key: val for key, val in response.POST.items() if key.startswith('home_goal_')}
            away_players_goals = {key: val for key, val in response.POST.items() if key.startswith('away_goal_')}

            save_match(home_players_goals, away_players_goals, context_match,
                       home_goals, away_goals, yellows, reds, deleted_from_disqualified)
            return HttpResponseRedirect(
                "/view-match/%s/%i" % (context_match["match"].tournament.uid, context_match["match"].id))

    return render(response, "main/add_score.html", context_match)


def view_match(response, uid, match_id):
    context = get_match_context(response.user, uid, match_id)
    print(context["match"].stage)
    if response.POST.get("delete") and context['access']:
        delete_match(context['match'])
        return HttpResponseRedirect("/add-score/%s/%i" % (uid, match_id))

    return render(response, "main/view_match.html", context)


def tournament_admins(response, uid):
    try:
        tournament = Tournament.objects.get(uid=uid)
    except ObjectDoesNotExist:
        raise Http404

    if tournament.owner != response.user:
        raise PermissionDenied

    admins = tournament.admins.all()
    error = ""

    if response.method == "POST" and tournament.owner == response.user:
        if response.POST.get("add-admin"):
            try:
                new_admin = User.objects.get(username=response.POST.get("name-admin"))
                tournament.admins.add(new_admin)
                tournament.save()
            except ObjectDoesNotExist:
                error = "Такого пользователя не существует"
        if response.POST.get("del-admins"):
            list_for_del = response.POST.getlist("delete-admin")
            for old_admin in list_for_del:
                tournament.admins.remove(User.objects.get(username=old_admin))
                tournament.save()

    return render(response, "main/admins.html", {"admins": admins,
                                                 "tournament": tournament,
                                                 "error": error})
