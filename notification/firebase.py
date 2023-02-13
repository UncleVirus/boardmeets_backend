from pyfcm import FCMNotification
from .models import FCMToken
from eboard_system import settings

FIREBASE_API_KEY = settings.FIREBASE_API_KEY

push_service = FCMNotification(api_key=FIREBASE_API_KEY)

def test_notif():
    push_service.notify_single_device(
                    registration_id='dT89esm5M9H3W9mcl335Em:APA91bFndXwDJSipwiDN-BDqPzF47Z5P3sdVNh3cqScTn11cjnjYk6J_Hbq2uuG09jl95YCNux1gnNmlCxNVv1VIJIGoI1OMczKDMjEfyTL7mB6v_i2-q3RZvfui9C9K95xaolrGeesS',
                    message_title = 'Hi Valens',
                    time_to_live=86400,
                    message_body='this is the test notification',
                    content_available=True,
                    delay_while_idle=True
                )

def send_single_notification(user, data):

    device = FCMToken.objects.filter(user=user).first()

    if device is not None:
        registration_id = device.registration_id

        try:
            push_service.notify_single_device(
                    registration_id=registration_id,
                    message_title = data['title'],
                    time_to_live=86400,
                    message_body=data,
                    content_available=True,
                    delay_while_idle=True
                )
        except:
            pass

def send_multiple_notification(users, data):

    devices = []
    for user_id in users:
        device = FCMToken.objects.filter(user=user_id).first()
        if device is not None:
            devices.append(device.registration_id)

    if devices is not None:
        try:
            push_service.notify_multiple_devices(
                    registration_ids=devices,
                    message_title = data['title'],
                    time_to_live=86400,
                    message_body=data,
                    content_available=True,
                    delay_while_idle=True
                )
        except:
            pass