from django.shortcuts import render
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from rest_framework.response import Response
from licenses.serializers import LicenseBodySerializer,LicenseCurrentUsersSerializer
from licenses.models import LicenseBody,LicenseCurrentUsers
from eboard_system.views import AuthenticatedAPIView
from rest_framework.views import APIView
import rsa
from base64 import b64encode
import random
from django.http import JsonResponse
import uuid
from getmac import get_mac_address as gma
from django.conf import settings
from django.contrib.auth.models import User

#Generate server key on installation
class GenerateServerKey(AuthenticatedAPIView):
    serializer_class = LicenseBodySerializer
    def post(self,request,format=None):
        server_id = uuid.uuid4()
        mac_address = gma()
        existing_mac = LicenseBody.objects.filter(mac_address=mac_address)
        if existing_mac:
            return Response({"data":"Server Already Registered"},status=HTTP_400_BAD_REQUEST)
        else:
            initial_license_data = LicenseBody.objects.create(
                server_id=server_id,mac_address=mac_address
            )
            return Response({"server_id":server_id},status=HTTP_201_CREATED)