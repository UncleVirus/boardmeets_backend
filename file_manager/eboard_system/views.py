from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView 
from rest_framework.permissions import IsAuthenticated


class AuthenticatedAPIView(GenericAPIView):
    permission_classes  = [IsAuthenticated]