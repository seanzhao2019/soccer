from __future__ import unicode_literals

from django.db import models

# Create your models here.
class MatchesInfo (models.Model):
    match_id=models.IntegerField(primary_key=True)
    match_code = models.CharField(max_length=30) #primary key will automatically
    date_of_match = models.DateTimeField(null=True)    
    team_home_goals = models.PositiveIntegerField()
    team_away_goals = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.match_code 


class TeamsInfo (models.Model):
    match = models.ForeignKey(MatchesInfo,on_delete=models.CASCADE)
#    id= models.AutoField(primary_key=True,default=1)
    team_code = models.CharField(max_length=30) #primary key
    country_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=30)    
    total_score = models.PositiveIntegerField()

    def __unicode__(self):
        return self.country_name


class CoachsInfo (models.Model):
    coach_code = models.IntegerField(primary_key=True)    #primary key
    coach_name = models.CharField(max_length=30)
    coach_birthday= models.DateField()
    coach_country = models.CharField(max_length=30)
    coach_team = models.OneToOneField(TeamsInfo,on_delete=models.CASCADE)

    def __unicode__(self):
        return self.coach_name


class PlayersInfo (models.Model):
    team = models.ForeignKey(TeamsInfo,on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachsInfo,on_delete=models.CASCADE)
    player_name = models.CharField(max_length=30)
    player_code = models.IntegerField(primary_key=True)    #primary key
    player_loc = models.CharField(max_length=30)
    player_height = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.player_name



class SponsorsInfo (models.Model):
    sponsor_name  = models.CharField(max_length=30) #primary key
    nasdaq= models.IntegerField(primary_key=True) 
    date_of_found = models.DateField()    
    sponsor_team = models.ManyToManyField(TeamsInfo,through='Relationship_Sponsors_teams')#m:n relationship
    def __unicode__(self):
        return self.sponsor_name 

class Relationship_Sponsors_teams (models.Model):
    team = models.ForeignKey(TeamsInfo,on_delete=models.CASCADE)
    sponsor = models.ForeignKey(SponsorsInfo,on_delete=models.CASCADE)
    date_of_sponsor  = models.DateField() 
    
    def __unicode__(self):
        return self.sponsor.sponsor_name

		