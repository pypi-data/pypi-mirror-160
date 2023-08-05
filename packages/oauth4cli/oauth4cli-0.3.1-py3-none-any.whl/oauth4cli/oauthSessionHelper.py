import base64
import hashlib
import requests

from random import random
from string import ascii_letters, digits


def get_random_string(str_size):
    chars = ascii_letters + digits + ".-_~"
    return ''.join(random.choice(chars) for x in range(str_size))


def get_well_known_metadata(well_known_url):
    response = requests.get(well_known_url)
    response.raise_for_status()
    return response.json()


class OauthSessionHelper(object):

    def __init__(self, well_known_url: str, client_id: str, scope: str="openid"):
        self.well_known = get_well_known_metadata(well_known_url)
        self.client_id = client_id
        self.scope = scope
        self.state = None
        self.nonce = None
        self.pkce_code_verifier = None

    def get_authorization_url(self, redirect_uri: str, pkce: bool = False):
        self.state = get_random_string(20)
        self.nonce = get_random_string(25)

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "state": self.state,
            "nonce": self.nonce,
            "scope": self.scope,
            "redirect_uri": redirect_uri
        }

        if pkce:
            self.pkce_code_verifier = get_random_string(45)
            code_digest = hashlib.sha256(self.pkce_code_verifier.encode('utf-8')).digest()
            code_challenge = base64.urlsafe_b64encode(code_digest).decode('utf-8').replace('=', '')
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"

        query_string = "&".join(f'{key}={value}' for key, value in params.items())
        auth_url = f"{self.well_known.get('authorization_endpoint')}?{query_string}"
        return auth_url
