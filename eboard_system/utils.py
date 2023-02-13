import random,string
from sendgrid import SendGridAPIClient
from eboard_system import settings


def generate_code():
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))    
    return key

def send_email(message):
    try:
        send_grid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        response = send_grid_client.send(message)
        return response.status_code

    except Exception as e:
        print(e)
        return False

