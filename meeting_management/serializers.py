from rest_framework import serializers

from accounts.models import User
from .models import Meeting, Minutes, Annotation, Rsvp, AgendaAction, MinutesAgenda, AgendaItem
from accounts.serializers import UserSerializer


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
        depth = 3


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'
        depth = 3


class AgendaActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaAction
        fields = '__all__'
        depth = 3


class AgendaItemSerializer(serializers.ModelSerializer):
    permission = UserSerializer(many=True)

    class Meta:
        model = AgendaItem
        fields = '__all__'


class MinutesAgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinutesAgenda
        fields = '__all__'
        depth = 3


class MinutesDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minutes
        fields = '__all__'
        depth = 3


class RSVPserialzier(serializers.ModelSerializer):
    class Meta:
        model = Rsvp
        fields = '__all__'
        depth = 2
