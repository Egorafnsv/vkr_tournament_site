from ..models import Matches, Playoff_scheme


def check_next_stage(stage):
    matches = Matches.objects.filter(playoff_stage=stage)

    stage_status = True
    for i in matches:
        if not i.status:
            stage_status = False

    if stage_status:
        if stage.home_goals > stage.away_goals:
            send_club_next(stage.tournament, stage.club_home, stage.stage)
        elif stage.home_goals < stage.away_goals:
            send_club_next(stage.tournament, stage.club_away, stage.stage)


def send_club_next(tournament, club, stage):
    stage = stage.split("_")
    stage[0] = int(stage[0]) // 2
    stage[1] = int(stage[1]) // 2

    next_stage_str = str(stage[0]) + "_" + str(stage[1])

    next_stage = Playoff_scheme.objects.filter(tournament=tournament).get(stage=next_stage_str)

    if not next_stage.club_home:
        next_stage.club_home = club
    else:
        next_stage.club_away = club
        for num in range(tournament.rounds):
            new_match = Matches(tournament=tournament,
                                playoff_stage=next_stage,
                                club_home=next_stage.club_home,
                                club_away=club,
                                stage=stage[0] + stage[1],
                                text_stage=f"1/{stage[0]}",
                                serial_number=num)
            new_match.save()

            if stage[0] == 1:
                break

    next_stage.save()
