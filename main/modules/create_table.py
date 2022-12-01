from django.db.models import Q

from ..models import Clubs, Matches


def get_sort_tables(table, rules):
    table = [j for j in [i for i in table.values('club_id', 'win', 'draw', 'lose',
                                                 'goals_for', 'goals_against', 'goals_difference', 'points')]]

    rules = rules.split("_")

    for i in range(len(table) - 1):
        # алгоритм выбором
        index = i
        for j in range(i + 1, len(table)):
            if table[j]['points'] > table[index]['points']:
                index = j
            elif table[j]['points'] == table[index]['points']:
                if compare_by_other_val(table[j], table[index], rules): index = j

        table[i], table[index] = table[index], table[i]

    table_sorted = []

    for i in table:
        row = list(i.values())
        row.insert(1, str(Clubs.objects.get(id=i['club_id'])))
        table_sorted.append(row)

    return table_sorted


def compare_by_other_val(team_j, team_index, rules):
    for i in rules:
        if i == "GD":
            if team_j["goals_difference"] > team_index["goals_difference"]:
                return True
            elif team_j["goals_difference"] < team_index["goals_difference"]:
                return False
            else:
                continue
        elif i == "GF":
            if team_j["goals_for"] > team_index["goals_for"]:
                return True
            elif team_j["goals_for"] < team_index["goals_for"]:
                return False
            else:
                continue
        elif i == "GA":
            if team_j["goals_against"] < team_index["goals_against"]:
                return True
            elif team_j["goals_against"] > team_index["goals_against"]:
                return False
            else:
                continue
        elif i == "W":
            if team_j["win"] > team_index["win"]:
                return True
            elif team_j["win"] < team_index["win"]:
                return False
            else:
                continue
        elif i == "L":
            if team_j["lose"] < team_index["lose"]:
                return True
            elif team_j["lose"] > team_index["lose"]:
                return False
            else:
                continue
        elif i == "HTH":
            goals_j = 0
            goals_index = 0
            for match in Matches.objects.filter(Q(club_home=team_j["club_id"]) & Q(club_away=team_index["club_id"])):
                goals_j += match.home_goals
                goals_index += match.away_goals

            for match in Matches.objects.filter(Q(club_home=team_index["club_id"]) & Q(club_away=team_j["club_id"])):
                goals_j += match.away_goals
                goals_index += match.home_goals

            if goals_j > goals_index:
                return True
            elif goals_j < goals_index:
                return False
            else:
                continue

    return False


def create_playoff_grid(playoffs_query):
    grid = []
    for stage in playoffs_query:
        current_stage = stage.stage.split("_")
        current_stage = [int(i) for i in current_stage]
        current_text_stage = " final" if current_stage[0] == 1 else f"1/{current_stage[0]} branch №{current_stage[1]}"
        next_text_stage = " final" if current_stage[0]//2 <= 1 else f"1/{current_stage[0]//2} branch №{current_stage[1]//2}"

        club_home = stage.club_home if stage.club_home else "(Неизвестен)"
        club_away = stage.club_away if stage.club_away else "(Неизвестен)"
        club_home_id = stage.club_home.id if stage.club_home else 0
        club_away_id = stage.club_away.id if stage.club_away else 0

        grid.append([current_text_stage, club_home, stage.home_goals, stage.away_goals, club_away,
                     next_text_stage, club_home_id, club_away_id])

        grid.sort(reverse=True)

    return grid
