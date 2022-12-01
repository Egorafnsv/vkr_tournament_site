from django.db.models import Q
from django.test import TestCase

# Create your tests here.
from main.models import *
from main.modules.check_next_stage import check_next_stage
from main.modules.create_table import get_sort_tables
from main.modules.create_tournament import create_clubs_and_schedule
from main.modules.delete_match import delete_match
from main.modules.save_match import save_result


class CreateLeagueTestCase(TestCase):
    def setUp(self):
        count_clubs = 3
        self.tournament = Tournament(name="test", type="L", rounds=2, count_clubs=count_clubs,
                                     distribution_rules="GD_GF_GA")
        self.tournament.save()
        list_clubs = ["Team" + str(i) for i in range(1, count_clubs + 1)]
        create_clubs_and_schedule(list_clubs, self.tournament, False)

    def test_create_clubs(self):
        self.assertEqual(self.tournament.count_clubs, len(Clubs.objects.filter(tournament=self.tournament)))

    def test_create_matches(self):
        matches = Matches.objects.filter(tournament=self.tournament)

        matches_in_tour = self.tournament.count_clubs - 1 if self.tournament.count_clubs % 2 == 0 else self.tournament.count_clubs
        count_matches = (self.tournament.count_clubs // 2 * matches_in_tour) * self.tournament.rounds

        self.assertEqual(count_matches, len(matches))

    def test_schedules(self):
        matches = Matches.objects.filter(tournament=self.tournament)
        clubs = Clubs.objects.filter(tournament=self.tournament)

        check = True

        for m in matches:
            if m.club_home == m.club_away:
                check = False
                break

        for i in range(len(clubs)):
            if not check:
                break

            club_1 = clubs[i]
            for j in range(i + 1, len(clubs)):
                club_2 = clubs[j]
                count_matches = len(matches.filter(
                    (Q(club_home=club_1) & Q(club_away=club_2)) | (Q(club_home=club_2) & Q(club_away=club_1))))
                if count_matches != self.tournament.rounds:
                    check = False
                    break

        self.assertTrue(check)

    def test_update_table(self):
        club = Clubs.objects.get(tournament=self.tournament, name="Team1")
        match = Matches.objects.filter(stage=2).get(Q(club_home=club) | Q(club_away=club))
        save_result(match, 5, 2)
        table_record = Tables.objects.get(tournament=self.tournament, club=club)

        self.assertEqual(3, table_record.points)

    def test_delete_match(self):
        club = Clubs.objects.get(tournament=self.tournament, name="Team1")
        match = Matches.objects.filter(stage=2).get(Q(club_home=club) | Q(club_away=club))
        match.actions = ":::"
        match.save()
        save_result(match, 5, 2)

        delete_match(match)

        table_record = Tables.objects.get(tournament=self.tournament, club=club)

        self.assertEqual(0, table_record.points)

    def test_sort_table(self):
        matches = Matches.objects.filter(tournament=self.tournament)

        club_1 = Clubs.objects.filter(tournament=self.tournament).get(name="Team1")
        club_2 = Clubs.objects.filter(tournament=self.tournament).get(name="Team2")
        club_3 = Clubs.objects.filter(tournament=self.tournament).get(name="Team3")

        club1_vs_club2 = matches.filter(Q(club_home=club_1) & Q(club_away=club_2))[0]
        club1_vs_club3 = matches.filter(Q(club_home=club_1) & Q(club_away=club_3))[0]
        club2_vs_club3 = matches.filter(Q(club_home=club_2) & Q(club_away=club_3))[0]

        save_result(club1_vs_club2, 1, 3)
        save_result(club1_vs_club3, 2, 2)
        save_result(club2_vs_club3, 4, 1)

        tables = get_sort_tables(Tables.objects.filter(tournament=self.tournament), self.tournament.distribution_rules)

        result = [i[1] for i in tables[:3]]

        result_expected = ["Team2", "Team1", "Team3"]

        self.assertEqual(result_expected, result)


class CreatePlayoffTestCase(TestCase):
    def setUp(self):
        count_clubs = 6
        self.tournament = Tournament(name="test", type="P", rounds=2, count_clubs=count_clubs)
        self.tournament.save()
        list_clubs = ["Team" + str(i) for i in range(1, count_clubs + 1)]
        create_clubs_and_schedule(list_clubs, self.tournament, False)

    def test_scheme(self):
        club_1 = Clubs.objects.get(name="Team1")
        club_2 = Clubs.objects.get(name="Team2")
        stages_club_1 = Playoff_scheme.objects.filter(tournament=self.tournament).get(
            (Q(club_home=club_1) | Q(club_away=club_1)))
        stages_club_2 = Playoff_scheme.objects.filter(tournament=self.tournament).get(
            (Q(club_home=club_2) | Q(club_away=club_2)))

        check = stages_club_1.stage == "2_0" and stages_club_2.stage == "2_1"

        self.assertTrue(check)

    def test_next_stage_false(self):
        check_next_stage(Playoff_scheme.objects.filter(tournament=self.tournament).get(stage="4_1"))
        self.assertFalse(Playoff_scheme.objects.filter(tournament=self.tournament).get(stage="2_0").club_away)

    def test_next_stage_true(self):
        stage = Playoff_scheme.objects.filter(tournament=self.tournament).get(stage="4_1")
        matches = Matches.objects.filter(tournament=self.tournament).filter(playoff_stage=stage)

        for m in matches:
            m.status = True
            m.save()

        stage.home_goals = 5
        stage.away_goals = 2
        stage.save()

        win_club = stage.club_home

        check_next_stage(stage)

        win_club_is_next_stage = win_club == Playoff_scheme.objects.filter(tournament=self.tournament).get(stage="2_0").club_away

        self.assertTrue(win_club_is_next_stage)
