import json
import os
from datetime import datetime

from app.auth import AUTH0_DOMAIN, AUTH0_APP_AUDIENCE, AUTH0_CLIENT_ID, \
    AUTH0_CLIENT_SECRET, AUTH0_CLIENT_ID1, AUTH0_CLIENT_SECRET1, \
    AUTH0_CLIENT_ID2, AUTH0_CLIENT_SECRET2, verify_decode_jwt


def generate_token_by_role(role):
    """Generate token per role: ['student','teacher'] for Auth0"""
    payloads = {
        'student': {
            'client_id': AUTH0_CLIENT_ID1,
            'client_secret': AUTH0_CLIENT_SECRET1,
            'audience': AUTH0_APP_AUDIENCE,
            'grant_type': 'client_credentials'
        },
        'teacher': {
            'client_id': AUTH0_CLIENT_ID2,
            'client_secret': AUTH0_CLIENT_SECRET2,
            'audience': AUTH0_APP_AUDIENCE,
            'grant_type': 'client_credentials'
        }
    }
    try:
        conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
        headers = {'content-type': "application/json"}
        payload = payloads[role]
        conn.request("POST", "/oauth/token", json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data)
    except:
        return None


def load_tokens():
    """Load tokens from the filesystem for Auth0 to prevent network issues"""
    tokens_file = os.path.join(os.path.dirname(__file__), 'token.json')
    if os.path.exists(tokens_file):
        with open(tokens_file) as f:
            return json.load(f)
    return None


def verify_token_exp(token):
    """Verify that the token have not expired for Auth0"""
    payload = verify_decode_jwt(token)
    return datetime.fromtimestamp(payload['exp']) > datetime.now()