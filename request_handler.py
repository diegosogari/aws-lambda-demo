import logging
import json
import jwt
import os
import functools
import requests

jwks_url = "https://{}/.well-known/jwks.json".format(os.environ["USER_POOL_ENDPOINT"])
pkeys_url = "https://public-keys.auth.elb.{}.amazonaws.com/".format(os.environ["AWS_REGION"])

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
logger.info("JWKS: %s", jwks_url)
logger.info("PKEYS: %s", pkeys_url)

jwks = jwt.PyJWKClient(jwks_url)

def handle(event, context):
    logger.debug(json.dumps(event))

    email = handle_auth(event["headers"])
    if email:
        logger.info("Email: %s", email)

    body = json.loads(event["body"])
    reply = {
        "message": "Hello {}!".format(body["name"])
    }
    if email:
        reply["email"] = email
    return {
        "statusCode": 200,
        "body": json.dumps(reply)
    }

def handle_auth(headers: dict) -> str:
    if "x-amzn-oidc-accesstoken" in headers:
        token = headers["x-amzn-oidc-accesstoken"]
        verify_access_token(token)

    if "x-amzn-oidc-data" in headers:
        token = headers["x-amzn-oidc-data"]
        claims = verify_user_claims(token)
        return claims["email"]

    return None

def verify_access_token(token: str) -> str:
    skey = jwks.get_signing_key_from_jwt(token)
    return verify_token(token, skey.key, algorithms=["RS256"])

def verify_user_claims(token: str) -> str:
    header = jwt.get_unverified_header(token)
    pkey = get_public_key_from_url(header["kid"])
    return verify_token(token, pkey, algorithms=["ES256"])

def verify_token(token: str, key: str, algorithms: list[str]) -> str:
    try:
        payload = jwt.decode(token, key, algorithms)
    except Exception as e:
        raise Exception("could not verify token", token, str(e))
    else:
        logger.info("Token verified: %s", token)
        return payload

@functools.cache
def get_public_key_from_url(kid: str) -> str:
    try:
        return requests.get(pkeys_url + kid).text
    except Exception as e:
        raise Exception("could not load public key", kid, str(e))