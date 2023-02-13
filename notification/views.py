import imp
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import FCMToken

# Create your views here.

@api_view(['PATCH', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def register_user_device(request):
    user = request.user.id

    """
    Should receive fcm registration id and user instance
    
    """
    try:
        message = 'Device has been created. '
        device, created = FCMToken.objects.get_or_create(
            user=user,
            registration_id=request.data['registration_id']
        )
        if not created:
            device.registration_id = request.data['registration_id']
            device.save()
            message = 'Device has been updated. '

        return Response(message, status=200)

    except Exception as e:
        return Response({"detail": str(e)}, status=400)
