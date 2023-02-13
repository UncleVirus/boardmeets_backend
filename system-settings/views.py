from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from system_settings.models import License, Orgdescription, Orgname
from system_settings.serializers import LicenseSerializer, OrgdescriptionSerializer
from system_settings.models import Missionstatement
from system_settings.serializers import MissionstatementSerializer
from system_settings.models import Vissionstatement
from system_settings.serializers import VissionstatementSerializer
from system_settings.serializers import BoardleadersSerializer
from system_settings.models import Boardleaders
from system_settings.models import Sociallinks
from system_settings.serializers import SociallinksSerializer
from system_settings.serializers import OrgnameSerializer
from system_settings.models import Orgname
from system_settings.models import License
from system_settings.serializers import LicenseSerializer

class OrgnameViewSet(viewsets.ModelViewSet):
    queryset = Orgname.objects.all()
    serializer_class = OrgnameSerializer

class OrgdescriptionViewSet(viewsets.ModelViewSet):
    queryset = Orgdescription.objects.all()
    serializer_class = OrgdescriptionSerializer

class MissionstatementViewSet(viewsets.ModelViewSet):
    queryset = Missionstatement.objects.all()
    serializer_class = MissionstatementSerializer

class VissionstatementViewSet(viewsets.ModelViewSet):
    queryset = Vissionstatement.objects.all()
    serializer_class = VissionstatementSerializer


class BoardleadersViewSet(viewsets.ModelViewSet):
   queryset = Boardleaders.objects.all()
   serializer_class = BoardleadersSerializer

class SociallinksViewSet(viewsets.ModelViewSet):
   queryset = Sociallinks.objects.all()
   serializer_class = SociallinksSerializer

class LicenseViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer



