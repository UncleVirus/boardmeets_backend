import jwt
import requests
import json
from eboard_system import settings
import time as timestamp
import hashlib
import hmac
import base64
from time import time

# create a function to generate a token
# using the pyjwt library

def generateToken():
    token = jwt.encode(
        # Create a payload of the token containing
        # API Key & expiration time
        {'iss':settings.API_KEY, 'exp': time() + 5000},
 
        # Secret used to generate token signature
        settings.API_SEC,
 
        # Specify the hashing alg
        algorithm='HS256'
    )
    return token


def createMeeting(meetingdetails):
    headers = {'authorization': 'Bearer ' + generateToken(),
               'content-type': 'application/json'}
    try:
        r = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings',
            headers=headers, data=json.dumps(meetingdetails))

        meeting_data = json.loads(r.text)
        return meeting_data

    except Exception as e:
        return False


def generateSignature(sig_ingredients):
    try:
        mtg_number: str = str(sig_ingredients['meetingNumber'])
        api_key: str = str(sig_ingredients['apiKey'])
        role: str = str(sig_ingredients['role'])
        api_secret: bytes = bytes(str(sig_ingredients['apiSecret']), 'utf-8')

        ts: str = str(int(round(timestamp.time() * 1000)) - 30000)
        msg: str = api_key + mtg_number + ts + role
        message: base64 = base64.b64encode(bytes(msg, 'utf-8'))

        hash_value = hmac.new(api_secret, message, hashlib.sha256)
        hash_value = base64.b64encode(hash_value.digest())
        hash_value: hashlib = hash_value.decode("utf-8")
        tmp_string: str = f"{api_key}.{mtg_number}.{ts}.{role}.{hash_value}"
        signature: bytes = base64.b64encode(bytes(tmp_string, "utf-8"))
        signature: str = signature.decode("utf-8").rstrip("=")

        return signature

    except Exception as e:
        return False
