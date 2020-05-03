import http.client
import json
import os
import time
from datetime import datetime, timedelta
from functools import wraps
import random
from urllib.request import urlopen

from authlib.integrations.flask_client import OAuth
from flask import request, abort, session
from jose import jwt

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
AUTH0_APP_AUDIENCE = os.environ.get('AUTH0_APP_AUDIENCE')
AUTH0_ALGORITHM = ['RS256']
AUTH0_API_MANAGEMENT = os.environ.get('AUTH0_API_MANAGEMENT')
# Alternate client id and client secret used for testing purposes
# Students rights
AUTH0_CLIENT_ID1 = os.environ.get('AUTH0_CLIENT_ID1')
AUTH0_CLIENT_SECRET1 = os.environ.get('AUTH0_CLIENT_SECRET1')
# Teachers rights
AUTH0_CLIENT_ID2 = os.environ.get('AUTH0_CLIENT_ID2')
AUTH0_CLIENT_SECRET2 = os.environ.get('AUTH0_CLIENT_SECRET2')


# AuthError Exception
class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def init_auth(app):
    oauth = OAuth(app)
    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=f'https://{AUTH0_DOMAIN}',
        access_token_url=f'https://{AUTH0_DOMAIN}/oauth/token',
        authorize_url=f'https://{AUTH0_DOMAIN}/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
        audience=AUTH0_APP_AUDIENCE
    )
    return oauth, auth0


def load_jwks():
    """
    This method is very tied to Auth0 authentication server.

    The JSON Web Key Set (JWKS) is a set of keys which contains the public
    keys used to verify any JSON Web Token (JWT) issued by the authorization
    server.
    Try to load the file from the filesystem and if this fails load it from
    the network.
    """
    # try to load the data locally
    jwks_file = os.path.join(os.path.dirname(__file__),
                             f'{AUTH0_DOMAIN}_jwks.json')
    if os.path.exists(jwks_file):
        jwks_contents = open(jwks_file).read()
    else:
        try:
            jwks_contents = urlopen(
                f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
            ).read()
            with open(jwks_file, 'wb') as f:
                f.write(jwks_contents)
        except Exception as e:
            print('error:', e)
            raise AuthError({
                'code': 'could_not_read_jwks',
                'description': e.message
            }, 401)
    return json.loads(jwks_contents)


def verify_decode_jwt(token):
    """
    Verify and decode the JWT Token. Than returns the payload.
    :param token: a json web token (string)
    :return: The decoded payload if no errors
    """
    # Load JWKS
    jwks = load_jwks()
    # Get the data in the header of the token (JWT=header.payload.signature)
    unv_head = jwt.get_unverified_header(token)
    # Get the RSA key from 'jkws' and compare it with the 'unv_head'
    rsa_key = {}
    if 'kid' not in unv_head:
        raise AuthError({
            'code': 'invalid_token_header',
            'description': 'Token header malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unv_head['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # finally use the key to validate the JWT
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=AUTH0_ALGORITHM,
                audience=AUTH0_APP_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Invalid claims error.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Invalid header.'
            }, 401)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Invalid header.'
    }, 401)


# Auth Header
def get_token_auth_header():
    """
    Attempt to get the header from the request
        raise an AuthError if no header is present
    Attempt to split bearer and the token
        raise an AuthError if the header is malformed
    :return: the token part of the header
    """
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'The authorization header is missing.'
        }, 401)
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The authorization header is invalid.'
        }, 401)
    return parts[1]


def check_permissions(permission, payload):
    """
    Check if the user has the permission.
    - Raise an AuthError if permissions are not included in the payload.
    - Raise an AuthError if the requested permission string is not in the
      payload permissions array.
    :param permission: string permission (i.e. 'post:drink')
                       list of permissions
    :param payload: decoded jwt payload
    :return: True if the user has the permission to do that action
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'Invalid claims.',
            'description': 'Permissions not included in JWT.'
        }, 400)
    # We should accept an array of permissions
    if type(permission) == str:
        permission = [permission]
    error = any(perm not in payload['permissions']
                for perm in permission)
    if error:
        raise AuthError({
            'code': 'unauthorized_access',
            'description': 'The user do not have permission to this resource.'
        }, 403)
    return True


def read_payload_from_token(token):
    if os.environ.get('config', 'default') != 'testing':
        payload = verify_decode_jwt(token)
    else:
        payload = decode_token(token)
    return payload


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = read_payload_from_token(token)
                check_permissions(permission, payload)
                return f(payload, *args, **kwargs)
            except AuthError as error:
                abort(error.status_code, description=error.error)

        return wrapper

    return requires_auth_decorator


def populate_user_infos(token, infos):
    """
    :param token: The token dictionary
    :param infos: The user infos dictionary
    :return:
    """
    from app.models import User  # Should be placed here

    PICTURE_HOST = 'https://randomuser.me/api/portraits/lego/'

    # Load the information stored in access token
    payload = read_payload_from_token(token['access_token'])
    # Load the information stored in database
    user = User.get_by_username(payload['sub'])
    # After first login
    # payload['permissions'] should be []
    # user should be None
    return {
        'token': token['access_token'],
        'expiration': payload['exp'],
        'permissions': payload['permissions'],
        'user_id': payload['sub'],
        'user_id_db': user.id if user is not None else None,
        'fullname': infos['name'] if user is None else user.fullname,
        'picture': (infos['picture'] if user is None
                    else user.picture if user.picture
                    else generate_random_picture()),
        'role': None if user is None else user.user_type
    }


class Auth0User:
    roles = {}

    def __init__(self, user_infos=None):
        self.user_infos = user_infos
        self.roles = {}
        self.user_id = None
        self.user_id_db = None
        self.expiry_date = datetime.now()  # expired date
        self.permissions = []
        self.picture = None
        self.fullname = None
        self.token = None

        if self.user_infos is not None:
            self.user_id = self.user_infos['user_id']
            self.user_id_db = self.user_infos['user_id_db']
            self.expiry_date = datetime.fromtimestamp(
                self.user_infos['expiration'])
            self.permissions = self.user_infos['permissions']
            self.picture = self.user_infos['picture']
            self.fullname = self.user_infos['fullname']
            self.role = self.user_infos['role']
            self.token = self.user_infos['token']

    def is_authenticated(self):
        return datetime.now() < self.expiry_date

    def has_role(self):
        return self.role is not None

    def has_permissions(self):
        return (self.permissions is not None
                and type(self.permissions) == list
                and len(self.permissions) > 0)

    def has_permission(self, permission):
        return (self.permissions is not None
                and type(self.permissions) == list
                and permission in self.permissions)

    @staticmethod
    def get_roles():
        """Get users 'role_id' from AUTH0 for student and teacher"""
        if Auth0User.roles != {}:
            return Auth0User.roles

        try:
            conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
            headers = {
                'content-type': "application/json",
                'Authorization': f'Bearer {AUTH0_API_MANAGEMENT}'
            }
            conn.request("GET", f"/api/v2/roles", None, headers)
            res = conn.getresponse()
            data = json.loads(res.read())
            roles = {}
            for item in data:
                if item['name'].lower() in ['student', 'teacher']:
                    roles[item['name'].lower()] = item['id']
            Auth0User.roles = roles
        except Exception as error:
            print(error)
            Auth0User.roles = {}
        return Auth0User.roles

    @staticmethod
    def set_role(user_id, role_id):
        """
        Assign the role_id corresponding to either 'student' or 'teacher'
        for the 'user_id'
        :return: True if the operation succeeds
        """
        try:
            conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
            headers = {
                'content-type': "application/json",
                'Authorization': f'Bearer {AUTH0_API_MANAGEMENT}'
            }
            conn.request("POST",
                         f"/api/v2/users/{user_id}/roles",
                         json.dumps({
                             "roles": [role_id]
                         }),
                         headers)

            res = conn.getresponse()
            # status = 204 -> role assigned
            return res.status == 204
        except:
            return False

    @staticmethod
    def get_permissions(user_id):
        permissions = []
        try:
            conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
            headers = {
                'content-type': "application/json",
                'Authorization': f'Bearer {AUTH0_API_MANAGEMENT}'
            }
            conn.request("GET",
                         f"/api/v2/users/{user_id}/permissions", None, headers)
            res = conn.getresponse()
            if res.status == 200:
                data = json.loads(res.read())
                permissions = [item['permission_name'] for item in data]
                return permissions
            return permissions
        except:
            return permissions


# This is used for local authentication when testing
PRIVATE_KEY_FILE = os.path.join(os.path.dirname(__file__), 'private.pem')
PUBLIC_KEY_FILE = os.path.join(os.path.dirname(__file__), 'public.pem')


def generate_key_pair():
    """Generate RS256 key pair"""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend

    # generate private/public key pair
    key = rsa.generate_private_key(backend=default_backend(),
                                   public_exponent=65537,
                                   key_size=2048)

    # get public key in PEM format
    public_key = (key.public_key()
                  .public_bytes(encoding=serialization.Encoding.PEM,
                                format=serialization.PublicFormat.PKCS1))

    # get private key in PEM container format
    pem = (key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()))

    # decode to printable strings
    private_key_str = pem.decode('utf-8')
    public_key_str = public_key.decode('utf-8')
    with open(PRIVATE_KEY_FILE, 'w') as f:
        f.write(private_key_str)
    with open(PUBLIC_KEY_FILE, 'w') as f:
        f.write(public_key_str)


def rs256_keys_exists():
    """Determine if the keys files are in the same directory"""
    return os.path.exists(PRIVATE_KEY_FILE) and os.path.exists(PUBLIC_KEY_FILE)


def generate_token(payload):
    """Generate a token using the local private key"""
    if not rs256_keys_exists():
        generate_key_pair()
    private_key_str = None
    with open(PRIVATE_KEY_FILE) as f:
        private_key_str = f.read()
    return jwt.encode(payload, private_key_str, algorithm=AUTH0_ALGORITHM[0])


def decode_token(token):
    """Decode the token using the local public key"""
    if not rs256_keys_exists():
        generate_key_pair()
    public_key_str = None
    with open(PUBLIC_KEY_FILE) as f:
        public_key_str = f.read()
    return jwt.decode(token, public_key_str, algorithms=AUTH0_ALGORITHM[0])


TEACHER_PERMISSIONS = [
    "archive:exams",
    "create:exams",
    "edit:exams",
    "enroll:exams",
    "list:exams",
    "list:students",
    "try-resolve:exams",
    "view-details:exams",
    "view-details:students"
]
STUDENT_PERMISSIONS = [
    "enroll:exams",
    "list:exams",
    "list:teachers",
    "try-resolve:exams",
    "view-details:teachers"
]


def generate_user_token(username, permissions):
    """Generate a token for a specific user"""
    timestamp = int(time.time())
    payload = {
        'sub': username,
        'iat': timestamp,
        'exp': timestamp + 86400,
        'permissions': permissions
    }
    return generate_token(payload)


def generate_user_infos(fullname):
    """Generate user infos dict with random image profile"""
    return {
        'name': fullname,
        'picture': generate_random_picture()
    }


def generate_random_picture():
    PICTURE_HOST = 'https://randomuser.me/api/portraits/lego/'
    return f'{PICTURE_HOST}{random.randint(0, 8)}.jpg'
