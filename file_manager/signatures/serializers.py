from rest_framework import serializers
from .models import Signature,DocumentsToBeSigned,DocumentSignatureAnnotation


class SignatureSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = '__all__'
        depth = 1

class DocuementsToBeSignedSerialzier(serializers.ModelSerializer):
    class Meta:
        model = DocumentsToBeSigned
        fields = '__all__'
        depth = 1

class DocumentSignatureAnnotationSerialzier(serializers.ModelSerializer):
    class Meta:
        model = DocumentSignatureAnnotation
        fields = '__all__'
        depth = 1