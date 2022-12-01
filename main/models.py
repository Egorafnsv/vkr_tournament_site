from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tournament(models.Model):
    TYPES = (('L', 'league'),
             ('P', 'playoff'),
             )

    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=20, default="trnmt-tmp")
    type = models.CharField(max_length=2, choices=TYPES)
    rounds = models.PositiveIntegerField(default=1)
    cards = models.PositiveIntegerField(default=4)
    distribution_rules = models.CharField(max_length=20, blank=True)
    count_clubs = models.PositiveIntegerField(null=False)
    owner = models.ForeignKey(User, related_name="tournament", on_delete=models.DO_NOTHING, null=True)
    admins = models.ManyToManyField(User, related_name="admins", blank=True)

    def __str__(self):
        return self.name


class Clubs(models.Model):
    name = models.CharField(max_length=15)
    notes = models.CharField(max_length=500, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Players(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    goals = models.PositiveIntegerField(default=0)
    yellow = models.PositiveIntegerField(default=0)
    red = models.PositiveIntegerField(default=0)
    disqualified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tables(models.Model):
    club = models.ForeignKey(Clubs, on_delete=models.SET_NULL, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    win = models.PositiveIntegerField(default=0)
    draw = models.PositiveIntegerField(default=0)
    lose = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    goals_difference = models.IntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.points = self.win * 3 + self.draw
        self.goals_difference = self.goals_for - self.goals_against
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.club)


class Playoff_scheme(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    club_home = models.ForeignKey(Clubs, on_delete=models.SET_NULL, null=True, blank=True, related_name="club_home_pl")
    club_away = models.ForeignKey(Clubs, on_delete=models.SET_NULL, null=True, blank=True, related_name="club_away_pl")
    home_goals = models.PositiveIntegerField(default=0)
    away_goals = models.PositiveIntegerField(default=0)
    stage = models.CharField(max_length=10)

    def __str__(self):
        return str(self.tournament) + ": stage " + str(self.stage) + " - " + str(self.club_home) + " - " + str(
            self.club_away)


class Matches(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    playoff_stage = models.ForeignKey(Playoff_scheme, null=True, blank=True, on_delete=models.CASCADE)
    club_home = models.ForeignKey(Clubs, on_delete=models.SET_NULL, null=True, related_name="club_home")
    club_away = models.ForeignKey(Clubs, on_delete=models.SET_NULL, null=True, related_name="club_away")
    home_goals = models.PositiveIntegerField(default=0)
    away_goals = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)
    stage = models.PositiveIntegerField()
    matchday = models.DateTimeField(null=True)
    text_stage = models.CharField(max_length=7, null=True, blank=True)
    serial_number = models.PositiveIntegerField(null=True, blank=True)
    actions = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.tournament) + ": stage " + str(self.stage) + " - " + str(self.club_home) + " - " + str(
            self.club_away)
