from rest_framework import serializers
from voting.models import VotingQuestion, Votes

class VotingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingQuestion
        fields = '__all__'
        depth = 1

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = '__all__'
        depth = 2