from rest_framework import serializers
from .models import ComplianceDetail,ChecklistDetail


class ComplianceDetailsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ComplianceDetail
        fields = '__all__'
        depth = 1

class ComplianceCheckListSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ChecklistDetail
        fields = '__all__'
        depth = 1