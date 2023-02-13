from django.db import models
from rest_framework import serializers
from .models import Folder, FolderDocument


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('__all__')
        depth = 1


class FolderDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderDocument
        fields = ('__all__')
        depth = 1
