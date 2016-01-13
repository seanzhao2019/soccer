from django.contrib import admin

# Register your models here.
from teams.models import TeamsInfo, CoachsInfo, PlayersInfo, MatchesInfo, SponsorsInfo, Relationship_Sponsors_teams
# Register your models here.


class TeamsInfoAdmin(admin.ModelAdmin):
    list_display = ('team_code', 'country_name', 'country_code', 'total_score')


class CoachsInfoAdmin(admin.ModelAdmin):
    list_display = ('coach_code', 'coach_name', 'coach_country', 'coach_team')


class PlayersInfoAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'player_code', 'player_loc',
                    'player_height', 'team', 'co')


class MatchesInfoAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'match_code',
                    'team_home_goals', 'team_away_goals')


class SponsorsInfoAdmin(admin.ModelAdmin):
    list_display = ('sponsor_name', 'nasdaq', 'loc_of_sponsor')


class Relationship_Sponsors_teamsAdmin(admin.ModelAdmin):
    list_display = ('team', 'sponsor', 'money_of_sponsor',
                    'years_of_contract', 'loc_of_contract')


admin.site.register(TeamsInfo, TeamsInfoAdmin)
admin.site.register(CoachsInfo, CoachsInfoAdmin)
admin.site.register(PlayersInfo, PlayersInfoAdmin)
admin.site.register(MatchesInfo, MatchesInfoAdmin)
admin.site.register(SponsorsInfo, SponsorsInfoAdmin)
admin.site.register(Relationship_Sponsors_teams,
                    Relationship_Sponsors_teamsAdmin)
