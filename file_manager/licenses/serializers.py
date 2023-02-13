from rest_framework import serializers
from licenses.models import LicenseBody,LicenseCurrentUsers
# from registration.serializers import OrganizationSerializer


class LicenseBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseBody
        # fields = '__all__'
        exclude = ('public_n','public_e','signature')

    # def to_representation(self, instance):
    #     serialized_data = super(LicenseBodySerializer,
    #                             self).to_representation(instance)
    #     details = OrganizationSerializer(
    #         instance.organization).data
    #     serialized_data['organization'] = details

    #     return serialized_data

class LicenseCurrentUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseCurrentUsers
        fields = '__all__'