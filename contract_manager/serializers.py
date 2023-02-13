from rest_framework import serializers
from .models import ContractDetail, ContractStage, ContractFeedBack, ContractSignature


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractDetail
        fields = '__all__'
        depth = 1


class ContractStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractStage
        fields = '__all__'
        depth = 1


class ContractFeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractFeedBack
        fields = '__all__'
        depth = 1


class ContractSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractSignature
        fields = '__all__'
        depth = 1
