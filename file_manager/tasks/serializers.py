from rest_framework import serializers
from .models import Tasks,Comments


class TaskSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'
        depth = 1

class CommentSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        depth = 1