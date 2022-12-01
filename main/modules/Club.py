from django.db.models import Q
from django.http import HttpResponseRedirect

from main.forms import CreateNewPlayer
from main.models import Clubs, Players, Matches


class Club:
    def __init__(self, club_id):
        self.club = Clubs.objects.get(id=club_id)
        self.tournament = self.club.tournament
        self.players = Players.objects.filter(club=club_id)
        self.matches = Matches.objects.filter(Q(club_home=club_id) | Q(club_away=club_id))

    def list_matches(self):
        matches_formatted = []
        if self.tournament.type == "L":
            for i in self.matches:
                if i.status:
                    matches_formatted.append((i.id, True, f"{i.stage} тур | {i.club_home} {i.home_goals}:{i.away_goals} {i.club_away}"))
                else:
                    matches_formatted.append((i.id, False, f"{i.stage} тур | {i.club_home} -:- {i.club_away}"))
        else:
            for i in self.matches:
                if i.status:
                    matches_formatted.append(
                        (i.id, True, f"{i.text_stage} | {i.club_home} {i.home_goals}:{i.away_goals} {i.club_away}"))
                else:
                    matches_formatted.append((i.id, False, f"{i.text_stage} | {i.club_home} -:- {i.club_away}"))

        matches_formatted.sort()

        return matches_formatted

    def get_free_numbers(self):
        taken_numbers = Players.objects.filter(club=self.club).values_list("number", flat=True)
        return [(str(i), i) for i in range(1, 100) if i not in taken_numbers]

    def add_players(self, response):
        form = CreateNewPlayer(self.get_free_numbers(), response.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            number = form.cleaned_data["number"]

            player = Players(number=number, name=name, club=self.club)
            player.save()

    def delete_players(self, players_for_delete):
        for id_player in players_for_delete:
            Players.objects.get(id=id_player).delete()

    def add_notes(self, text):
        self.club.notes = text
        self.club.save(update_fields=["notes"])
