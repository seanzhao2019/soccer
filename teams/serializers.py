from rest_framework import serializers
from teams.models import TeamsInfo , CoachsInfo ,PlayersInfo , MatchesInfo , SponsorsInfo , Relationship_Sponsors_teams

class MatchesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchesInfo
        fields = ('match_id', 'match_code', 'date_of_match', 'team_home_goals', 'team_away_goals')
  #  pk = serializers.IntegerField(read_only=True)
  #  match_code = serializers.CharField(max_length=30)
  #  date_of_match = serializers.DateTimeField()
  #  team_home_goals = serializers.IntegerField(min_value=0)
  #  team_away_goals = serializers.IntegerField(min_value=0)

    def create(self, validated_data):
        """
        Create and return a new `MatchesInfo` instance, given the validated data.
        """
        return MatchesInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `MatchesInfo` instance, given the validated data.
        """
        instance.match_code = validated_data.get('match_code', instance.match_code)
        instance.date_of_match = validated_data.get('date_of_match', instance.date_of_match)
        instance.team_home_goals = validated_data.get('team_home_goals', instance.team_home_goals)
        instance.team_away_goals = validated_data.get('team_away_goals', instance.team_away_goals)
        instance.save()
        return instance