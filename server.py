import requests
import json
import base64
import logging
from sys import exit as sys_ex

# Possible to connect with payload+token and just token


class SatisfactoryServer:
    """_summary_"""

    def __init__(self, address: str, port: int, key: str):
        """_summary_

        Args:
            address (str): _description_
            port (int): _description_
            key (str): _description_

        Raises:
            ConnectionError: _description_
        """
        self.logger = logging.getLogger("Server-Connect")
        logging.basicConfig(
            filename="serverConnect.log", encoding="utf-8", level=logging.DEBUG
        )
        # Do initial connection, verify token
        self.address = address + ":" + str(port) + "/api/v1"
        self.logger.info(f"Connecting to {self.address}...")
        if len(key.split(".")) > 1:
            # payload + token
            tokenPayload = key.split(".")[0]

            try:
                decodedPayload = base64.b64decode(tokenPayload)
            except "binascii.Error":
                self.logger.fatal(
                    "Provided token payload is not Base 64 encoded. Exiting..."
                )
                sys_ex()

            try:
                authLevel = json.loads(decodedPayload)["pl"]
            except KeyError:
                self.logger.fatal(
                    "Provided token payload is invalid. Did you provide a Satisfactory Server API Token?"
                )
                sys_ex()

        self.headers = {"Encoding": "utf-8", "Authorization": f"Bearer {key}"}
        initResponse = self._postJSONRequest(
            self.headers,
            payload=json.dumps({"function": "VerifyAuthenticationToken"}),
        )
        if initResponse.status_code == requests.status_codes.no_content:
            self.logger.info("Connection Successful")
            self.logger.info(f"Authenticated with {authLevel} privilege")
        else:
            self.logger.error(
                f"Connection to {address} failed with status {initResponse.status_code}!"
            )
            raise ConnectionError(
                f"Connection to {address} failed with status {initResponse.status_code}!"
            )

    def __str__(self):
        """_summary_"""
        pass

    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return f"SatisfactoryServer('{self.address}', '{self.key}')"

    def _postJSONRequest(self, headers: dict, payload: dict) -> requests.Response:
        """_summary_

        Args:
            headers (dict): _description_
            payload (dict): _description_

        Returns:
            requests.Response: _description_
        """
        response = requests.post(
            self.address, headers=headers, json=payload, verify=False
        )
        return response

    def passwordlessLogin(self, headers: dict) -> tuple:
        """_summary_

        Args:
            headers (dict): _description_

        Returns:
            tuple: _description_
        """
        payload = json.dumps(
            {
                "function": "PasswordlessLogin",
                "data": {"MinimumPrivilegeLevel": "client"},
            }
        )
        headers.update({"Content-Type": "application/json"})
        # Uses data=payload not, json=payload
        response = self._postJSONRequest(headers, payload)
        if response.status_code == requests.codes.ok:
            # Strip out auth token
            respJSON = response.json()
            authToken = respJSON["data"]["authenticationToken"]
            return (1, authToken)
        else:
            return (0, response.status_code)


server = SatisfactoryServer("192.168.1.17", 7777, "ewoJInAiOiAiQVBJVG9rZW4iCn0=")

# server = SatisfactoryServer(
#     "192.168.1.17",
#     "ewoJInBsIjogIkFQSVRva2VuIgp9.8A737E3138243B97CE20CA13BC1A8075EDFBF1FFA88EA7797A4AB9BF2683495B47286F2188769B50B43ECC6E0C8210F18F8A85F649EED540230AFAA685958711",
# )
