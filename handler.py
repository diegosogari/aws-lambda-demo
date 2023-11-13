import logging
import json
import jwt
import os
import functools
import requests

jwks_url = "https://{}/.well-known/jwks.json".format(os.environ["USER_POOL_ENDPOINT"])
pkeys_url = "https://public-keys.auth.elb.{}.amazonaws.com/".format(os.environ["AWS_REGION"])

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("JWKS: %s", jwks_url)
logger.info("PKEYS: %s", pkeys_url)

jwks = jwt.PyJWKClient(jwks_url)

def handle(event, context):
    email = handle_auth(event["headers"])
    if email:
        logger.info("Email: %s", email)

    body = json.loads(event["body"])
    reply = {
        "message": "Hello {}!".format(body["name"])
    }
    return {
        "statusCode": 200,
        "body": json.dumps(reply)
    }

def handle_auth(headers: dict) -> str:
    if "x-amzn-oidc-accesstoken" in headers:
        token = headers["x-amzn-oidc-accesstoken"]
        skey = jwks.get_signing_key_from_jwt(token)
        jwt.decode(token, skey.key, algorithms=["RS256"])

    if "x-amzn-oidc-data" in headers:
        token = headers["x-amzn-oidc-data"]
        pkey = get_key(jwt.get_unverified_header(token)["kid"])
        payload = jwt.decode(token, pkey, algorithms=["ES256"])
        return payload["email"]
    
    return None

@functools.cache
def get_key(kid: str) -> str:
    try:
        return requests.get(pkeys_url + kid).text
    except Exception as e:
        raise Exception("could not load public key", kid, str(e))