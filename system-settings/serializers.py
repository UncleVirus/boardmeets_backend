from rest_framework import serializers

from system_settings.models import License, Missionstatement
from system_settings.models import Boardleaders
from system_settings.models import Vissionstatement
from system_settings.models import Orgdescription
from system_settings.models import Sociallinks
from system_settings.models import Orgname
from system_settings.models import License

class OrgnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orgname
        fields = ('orgname',)

class OrgdescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orgdescription
        fields = ('orgdescription',)

class MissionstatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missionstatement
        fields = ('missionstatement',)

class VissionstatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vissionstatement
        fields = ('vissionstatement',)


class BoardleadersSerializer(serializers.ModelSerializer):
   class Meta:
       model = Boardleaders
       fields = ('chairman', 'ceo', 'secretary')

class SociallinksSerializer(serializers.ModelSerializer):
   class Meta:
       model = Sociallinks
       fields = ('facebook', 'twitter', 'linkedin')

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ('companyname', 'serverid', 'licensekey', 'expiryperiod')