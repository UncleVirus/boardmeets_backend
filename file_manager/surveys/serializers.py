from rest_framework import serializers
from .models import Survey, SurveyQuestions, SurveyResponses, SurveyRepondents


class AddSurveySerialzier(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'
        depth = 1


class ListSurveySerialzier(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'
        depth = 1


class QuestionSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestions
        fields = '__all__'
        depth = 2


class ResponsesSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponses
        fields = '__all__'
        depth = 1


class RespondentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyRepondents
        fields = '__all__'
        depth = 1
