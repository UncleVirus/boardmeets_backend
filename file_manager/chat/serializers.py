from chat.models import Message,Chat,Contact
from rest_framework import serializers
from django.contrib.auth.models import User

class ChatSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        depth = 3

class ContactSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        depth = 3

class MessageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        depth = 1

class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'