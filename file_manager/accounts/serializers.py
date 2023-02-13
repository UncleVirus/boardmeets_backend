from rest_framework import serializers
from .models import User,TwoFactorAuthentication,LoginAuditTrail,OrgGroup,OrganizationSetting,IpAddress,Department

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgGroup
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1
        extra_kwargs = {'password': {'write_only': True}}

class NormaUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('org_permission', 'org_groups','password')
        depth = 1

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "org_reference_key",
            "email",
            "password",
        ]
        depth = 1

class LoginAuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAuditTrail
        fields = '__all__'
        depth = 1

class IpAddresSerialzier(serializers.ModelSerializer):
    class Meta:
        model = IpAddress
        fields = '__all__'
        depth = 1

class IpfilteringSetting(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetting
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'