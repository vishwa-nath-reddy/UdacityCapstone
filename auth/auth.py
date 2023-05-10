import json
from flask import request, abort
from functools import wraps
from urllib.request import urlopen
import json
from six.moves.urllib.request import urlopen
from functools import wraps
# from crypto.PublicKey import RSA
from flask import Flask, request, jsonify, _request_ctx_stack, session
from flask_cors import cross_origin
# from jose import jwt
from os import environ as env
import jwt
import requests
from jwt.algorithms import RSAAlgorithm
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
ALGORITHMS = [env.get('ALGORITHMS')]
API_AUDIENCE = env.get('API_AUDIENCE')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

print('hello')


# class AuthError(Exception):
#     def __init__(self, error, status_code):
#         self.error = error
#         self.status_code = status_code

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'error': 'Cannot figure who authorized the transaction',
            'Problem': 'Could not found authorization'
        }, 422)
    auth_header = request.headers['Authorization']
    print(auth_header)
    header_parts = auth_header.split()
    if len(header_parts) != 2:
        raise AuthError({
            'error': 'JWT Compromised abort the operation',
            'Problem': 'Malicious script is being sent'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'error': '"Bearer" not found try again',
            'Problem': 'Check with your admin'
        }, 422)
    else:
        return header_parts[1]


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    print(permission, payload)
    if 'permissions' not in payload:
        raise AuthError({
            'error': 'JWT Compromised',
            'Problem': 'Retry in incognito'
        }, 400)
    ch = permission.split()
    for x in ch:
        if x != 'get:drinks' and x not in payload['permissions']:
            raise AuthError({
                'error': 'Permission Denied',
                'Problem': 'You do not have the permissiion to make requested changes'
            }, 403)
        else:
            return True
    # a = request.method.split()
    # result = [x.lower() for x in a]
    # checker = [y.split(':')[0] for y in payload['permissions']]
    # print(result, checker, payload, payload['permissions'])
    # for x in ch:
    # if result[0] not in checker:
    #     raise AuthError({
    #         'error': 'Permission Denied',
    #         'Problem': 'You do not have the permissiion to make requested changes'
    #     }, 403)
    # return True
    # raise Exception('Not Implemented')


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    print(token)
    print(2, token)
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    print(jsonurl)
    jwks = json.loads(jsonurl.read())
    print(jwks)
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'error': 'Missing id for the token',
            'Problem': 'JWT tampered'
        }, '400')
    print(unverified_header['kid'])
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            # rsa_key = key
    print(rsa_key)
    if rsa_key:
        try:
            public_key = RSAAlgorithm.from_jwk(json.dumps(rsa_key))
            # rsa_key2 = RSA.construct((int(rsa_key['n'], 16), int(rsa_key['e'], 16), int(rsa_key['d'], 16),
            #                          int(rsa_key['p'], 16), int(rsa_key['q'], 16)))

            print(10)
            # jwk = jwt.encode({'keys': [rsa_key]},headers=None, access_token=None)
            print(env.get("AUTH0_CLIENT_SECRET"))
            print(jwt.decode(
                token,
                public_key,
                algorithms='RS256',
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            ))
            # validator = PyJwtVerifier(jwt, auto_verify=False, custom_claim_name="custom_claim_value")
            # payload = validator.verify(True)
            # print(payload)
            print('semi')

            payload = jwt.decode(
                token,
                public_key,
                algorithms='RS256',
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            print('huddle finished')
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except Exception as e:
            print(e)
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(1)
            token = get_token_auth_header()
            print(2)
            payload = verify_decode_jwt(token)
            print(payload)
            print(3)
            check_permissions(permission, payload)
            print(payload)
            print(4)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
