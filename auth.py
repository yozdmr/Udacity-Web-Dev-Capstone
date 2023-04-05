from flask import Flask, request, abort, jsonify
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen

import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv(dotenv_path='authinfo.env')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')  # EX: example.us.auth0.com
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE')


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code



def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        abort(401, "Authorization header is expected.")
    
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        abort(401, 'Authorization header must start with "Bearer".')
    
    elif len(parts) == 1:
        abort(401, "Token not found.")

    elif len(parts) > 2:
        abort(401, "Authorization header must be bearer token.")

    token = parts[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400, "Authorization header is missing permission information.")

    if permission not in payload['permissions']:
        abort(403, "Authorization header is missing a required permission.")
    
    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        abort("Authorization malformed.")

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            abort(401, "Token expired.")

        except jwt.JWTClaimsError:
            abort(401, "Incorrect claims. Please, check the audience and issuer.")

        except Exception:
            abort(400, "Unable to parse authentication token.")
            
    abort(400, "Unable to find the appropriate key.")


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


# ------------------------------
# Error handlers
# ------------------------------
@app.errorhandler(400)
def autherror_400(error, message: str):
    return jsonify({
        "success": False,
        'error': 400,
        "message": message
    }), 400

@app.errorhandler(401)
def autherror_401(error, message: str):
    return jsonify({
        "success": False,
        'error': 404,
        "message": message
    }), 401

@app.errorhandler(403)
def autherror_403(error, message: str):
    return jsonify({
        "success": False,
        'error': 403,
        "message": message
    }), 403