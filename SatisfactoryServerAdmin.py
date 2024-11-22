import requests
import json
import base64
import logging
from sys import exit as sys_ex

# Possible to connect with payload+token and just token


class SatisfactoryServer:
    """Contains a reference to a running Satisfactory Dedicated Server. Provides certain management functions"""

    def __init__(self, address: str, key: str, port: int = 7777):
        """
        Initializes a new instance of the server object

        Args:
            address (str): The IP address (or FQDN) of the dedicated server
            key (str): The API key to be used when accessing the server. Can be either the API key + payload, or the bare key.
            port (int, optional): The port the server is running on. Defaults to 7777.

        Raises:
            ConnectionError: Raised if
        """
        self.logger = logging.getLogger("Server-Connect")
        logging.basicConfig(
            filename="serverConnect.log", encoding="utf-8", level=logging.DEBUG
        )
        # Do initial connection, verify token
        self.address = "https://" + address + ":" + str(port) + "/api/v1"
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
            payload={"function": "VerifyAuthenticationToken"},
        )
        # TODO: Raise different exception based on HTTP code
        if initResponse.status_code == requests.codes.no_content:
            self.logger.info("Connection Successful")
            self.logger.info(f"Authenticated with {authLevel} privilege")
        else:
            self.logger.error(
                f"Connection to {address} failed with status {initResponse.status_code}!"
            )
            raise ConnectionError(
                f"Connection to {address} failed with status {initResponse.status_code}!"
            )

    def __str__(self) -> str:
        """Retuns a human-readable string representation of the current object

        Returns:
            str: A string representation of the current object
        """
        return f"Satisfactory Server management instance for server at {self.address}"

    def __repr__(self) -> str:
        """
        Returns object constructor representation of the current object

        Returns:
           str: Object constructor representation of the current object
        """
        return f"SatisfactoryServer('{self.address}', '{self.key}')"

    def _postJSONRequest(self, headers: dict, payload: dict) -> requests.Response:
        """
        Sends an HTTP request to the server using a JSON formatted payload

        Args:
            headers (dict): A dict of standard HTTP headers to be included with the request
            payload (dict): A dict of dedicated server function data

        Returns:
            requests.Response: _description_
        """
        response = requests.post(
            self.address, headers=headers, json=payload, verify=False
        )
        return response

    def passwordlessLogin(self, headers: dict) -> tuple:
        """
        Performs a passwordless login to the server. Grants User level access.

        Args:
            headers (dict): Default HTTP headers of calling object

        Returns:
            tuple (int, string): (1, authToken) on success, (0, responseCode) on failure
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


if __name__ == "__main__":
    server = SatisfactoryServer(
        "192.168.1.17",
        "ewoJInBsIjogIkFQSVRva2VuIgp9.8A737E3138243B97CE20CA13BC1A8075EDFBF1FFA88EA7797A4AB9BF2683495B47286F2188769B50B43ECC6E0C8210F18F8A85F649EED540230AFAA685958711",
        7777,
    )
    print(
        server._postJSONRequest(
            server.headers, {"function": "enumerateSessions"}
        ).content
    )

# server = SatisfactoryServer(
#     "192.168.1.17",
#     "ewoJInBsIjogIkFQSVRva2VuIgp9.8A737E3138243B97CE20CA13BC1A8075EDFBF1FFA88EA7797A4AB9BF2683495B47286F2188769B50B43ECC6E0C8210F18F8A85F649EED540230AFAA685958711",
# )
