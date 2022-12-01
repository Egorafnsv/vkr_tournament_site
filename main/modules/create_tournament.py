from django.http import HttpResponseRedirect

from main.models import Tournament, Clubs, Tables, Matches, Playoff_scheme
from main.modules.generate_uid import generate
import random


def create_tournament(user, name, type_tournament, clubs, rounds, cards, rules_raw, shuffle):
    rules = get_rules(rules_raw, type_tournament)

    tournament = Tournament(name=name, type=type_tournament, count_clubs=len(clubs),
                            rounds=rounds, cards=cards, distribution_rules=rules)
    tournament.save()
    tournament.uid = generate()
    tournament.save(update_fields=['uid'])

    user.tournament.add(tournament)

    create_clubs_and_schedule(clubs, tournament, shuffle)

    return HttpResponseRedirect("/tournament/%s" % tournament.uid)


def get_rules(rules_raw, type_tournament):
    rules = ""

    if type_tournament == "L":
        table_parameters = sorted(list(rules_raw.keys()))

        rules = []

        for select in table_parameters:
            value = rules_raw[select]
            if value != "0" and value not in rules:
                rules.append(value)

        rules = "_".join(rules)

    return rules


def create_clubs_and_schedule(name_clubs, tournament, shuffle):
    clubs = []
    records_table = []

    for name in name_clubs:
        new_club = Clubs(name=name, tournament=tournament)
        clubs.append(new_club)

    Clubs.objects.bulk_create(clubs)

    if tournament.type != "P":
        for club in clubs:
            new_record_table = Tables(club=club, tournament=tournament)
            records_table.append(new_record_table)

        Tables.objects.bulk_create(records_table)
        create_league_schedule(clubs, tournament, shuffle)

    else:
        create_playoff_schedule(clubs, tournament, shuffle)


def create_league_schedule(list_clubs, tournament, shuffle):
    rounds = len(list_clubs)
    records_match = []

    if rounds % 2 != 0:
        list_clubs.append(None)  # "недостающий" участник для обычной генерации календаря с четным кол-м команд
        rounds += 1

    matches_per_round = rounds // 2

    for lap in range(tournament.rounds):
        if shuffle:
            random.shuffle(list_clubs)

        for i in range(1, rounds):
            for j in range(0, matches_per_round):
                if not (list_clubs[j] and list_clubs[-(j + 1)]):
                    continue
                new_match = Matches(tournament=tournament, club_home=list_clubs[j], club_away=list_clubs[-(j + 1)],
                                    stage=i + lap * rounds)

                records_match.append(new_match)

            list_clubs_tmp = list_clubs[1]
            for k in range(2, rounds):
                list_clubs[k - 1] = list_clubs[k]

            list_clubs[-1] = list_clubs_tmp

    Matches.objects.bulk_create(records_match)


def create_playoff_schedule(clubs, tournament, shuffle):
    # Для создания ассиметричной сетки, список команд "дополняется" null-командами до необходимого количества
    # для симметричной сетки, затем команды, играющие с null-командами, автоматически перемещаются в следующую стадию

    degree_of_two = 2
    users_number_clubs = len(clubs)

    # ближайшая верхняя степень двойки относительно количества команд пользователя
    while degree_of_two < users_number_clubs:
        degree_of_two *= 2

    count_null_teams = degree_of_two - users_number_clubs

    for i in range(count_null_teams):
        clubs.append(None)


    if shuffle:
        random.shuffle(clubs)

    number_clubs = len(clubs)
    start_stage = len(clubs) // 2
    playoff_list = []
    matches = []
    start = 4
    places_in_grid = [0, 1]

    while start < users_number_clubs:
        places_in_grid = list(map(lambda n: n*2, places_in_grid))

        tmp_array = list(map(lambda n: n+1, places_in_grid))
        tmp_array.reverse()

        places_in_grid += tmp_array
        start *= 2

    existing_stages = []  # для стадий, которые будут созданы в первом цикле и их не надо создавать в следующем

    for i in range(start_stage):
        if not clubs[number_clubs - i - 1]:
            next_stage = f"{start_stage // 2}_{places_in_grid[i] // 2}"

            if next_stage in existing_stages:
                for j in playoff_list:
                    if j.stage == next_stage:
                        j.club_away = clubs[i]
                        for num in range(tournament.rounds):
                            matches.append(Matches(tournament=tournament, playoff_stage=j,
                                                   club_home=j.club_home,
                                                   club_away=j.club_away,
                                                   stage=next_stage,
                                                   serial_number=num,
                                                   text_stage=f"1/{start_stage // 2}"))
                        break
            else:
                playoff_list.append(Playoff_scheme(tournament=tournament,
                                                   club_home=clubs[i],
                                                   club_away=None,
                                                   stage=next_stage))

                existing_stages.append(next_stage)
        else:
            playoff_list.append(Playoff_scheme(tournament=tournament,
                                               club_home=clubs[i],
                                               club_away=clubs[number_clubs - i - 1],
                                               stage=f"{start_stage}_{places_in_grid[i]}"))

            for num in range(tournament.rounds):
                matches.append(Matches(tournament=tournament, playoff_stage=playoff_list[-1],
                                       club_home=clubs[i], club_away=clubs[number_clubs - i - 1],
                                       serial_number=num,
                                       stage=(start_stage + places_in_grid[i]), text_stage=f"1/{start_stage}"))

    next_stage = start_stage // 2
    while True:
        for i in range(next_stage):
            if f"{next_stage}_{i}" in existing_stages:
                continue

            playoff_list.append(Playoff_scheme(tournament=tournament,
                                               club_home=None, club_away=None,
                                               stage=f"{next_stage}_{i}"))

        if next_stage <= 1:
            break
        else:
            next_stage //= 2

    Playoff_scheme.objects.bulk_create(playoff_list)
    Matches.objects.bulk_create(matches)
