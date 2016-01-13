from __future__ import unicode_literals

from django.db import models

# Create your models here.


class MatchesInfo (models.Model):
    match_id = models.IntegerField(primary_key=True)
    # primary key will automatically
    match_code = models.CharField(max_length=4)
#date_of_match = models.DateTimeField()
    team_home_goals = models.PositiveIntegerField()
    team_away_goals = models.PositiveIntegerField()

    def __unicode__(self):
        return self.match_code


class TeamsInfo (models.Model):
    m = models.ForeignKey(MatchesInfo, on_delete=models.CASCADE)
    team_code = models.IntegerField(primary_key=True)  # primary key
    country_name = models.CharField(max_length=2)
    country_code = models.IntegerField()
    total_score = models.PositiveIntegerField()

    def __unicode__(self):
        return self.country_name


class CoachsInfo (models.Model):
    coach_code = models.IntegerField(primary_key=True)  # primary key
    coach_name = models.CharField(max_length=4)
    coach_country = models.CharField(max_length=2)
    coach_team = models.OneToOneField(TeamsInfo, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.coach_name


class PlayersInfo (models.Model):
    team = models.ForeignKey(TeamsInfo, on_delete=models.CASCADE)
    co = models.ForeignKey(CoachsInfo, on_delete=models.CASCADE)
    player_code = models.IntegerField(primary_key=True) # primary key
    player_name = models.CharField(max_length=4)
    player_loc = models.CharField(max_length=30)
    player_height = models.PositiveIntegerField()

    def __unicode__(self):
        return self.player_name


class SponsorsInfo (models.Model):
    nasdaq = models.IntegerField(primary_key=True)# primary key
    sponsor_name = models.CharField(max_length=30)  
    loc_of_sponsor = models.CharField(max_length=30)
    sponsor_team = models.ManyToManyField(
        TeamsInfo, through='Relationship_Sponsors_teams')  # m:n relationship

    def __unicode__(self):
        return self.sponsor_name


class Relationship_Sponsors_teams (models.Model):
    team = models.ForeignKey(TeamsInfo, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(SponsorsInfo, on_delete=models.CASCADE)
    money_of_sponsor = models.IntegerField()
    years_of_contract = models.IntegerField()
    loc_of_contract = models.CharField(max_length=30)

    def __unicode__(self):
        return self.sponsor.sponsor_name
