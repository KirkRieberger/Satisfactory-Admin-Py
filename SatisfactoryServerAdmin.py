import requests
import json
import base64
import logging
from sys import exit as sys_ex

# Possible to connect with payload+token and just token

__author__ = "Kirk Rieberger"
__version__ = "0.0.1"
__date__ = "Nov 21, 2024"


class SatisfactoryServerAdmin:
    """Contains a reference to a running Satisfactory Dedicated Server. Provides certain management functions"""

    prettyPhase = {
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_1.GP_Project_Assembly_Phase_1'": "Distribution Platform",
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_2.GP_Project_Assembly_Phase_2'": "Construction Dock",
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_3.GP_Project_Assembly_Phase_3'": "Main Body",
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_4.GP_Project_Assembly_Phase_4'": "Propulsion",
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_5.GP_Project_Assembly_Phase_5'": "Assembly",
    }

    functions = [
        "HealthCheck",
        # Not useful - Returns if tick rate > 10
        "VerifyAuthenticationToken",
        # Returns nothing if healthy, insufficient_scope if bad
        "QueryServerState",
        # Returns general game info, requires auth
        "GetServerOptions",
        # Returns server management settings
        "GetAdvancedGameSettings",
        # Returns AGS, requires auth
        "ApplyAdvancedGameSettings",
        # Requires dict of settings to change
        "ClaimServer",
        # Returns new auth token without initial admin privileges.
        # Requires InitialAdmin privilege level, which can only be acquired by
        #   attempting passwordless login while the server does not have an
        #   Admin Password set. Requires new server name and admin password.
        "RenameServer",
        # Returns nothing on success.
        # Requires new server name
        "SetClientPassword",
        # Returns nothing on success.
        # Requires new client password IN PLAIN TEXT
        "SetAdminPassword",
        # Returns nothing on success.
        # Requires new admin password IN PLAIN TEXT and new token to use
        "SetAutoLoadSessionName",
        # Returns nothing on success.
        # Requires name of session to load
        "Run Command",
        # Returns output of command
        # Requires console command to run.
        "Shutdown",
        # Returns nothing on success.
        "ApplyServerOptions",
        # Requires dict of settings to change
        "CreateNewGame",
        # Returns nothing on success.
        # Requires dict of setup options
        "SaveGame",
        # Returns nothing on success.
        # Requires name of new save file
        "DeleteSaveFile",
        # Returns nothing on success.
        # Requires name of save file to delete
        "DeleteSaveSession",
        # Returns nothing on success.
        # Requires name of game session to delete
        "EnumerateSessions",
        # Returns array of sessions on server and index of loaded session.
        "LoadGame",
        # Returns nothing on success.
        # Requires name of save file to load and AGS enable bool
        "UploadSaveGame",
        # Requires name of save to upload, immediate load bool, AGS bool, and save
        #   file as multipart form request
        "DownloadSaveGame",
        # Returns save file.
        # Requires name of save file to download
    ]

    address = None

    loggedIn = False

    def __init__(self, address: str = None, token: str = None, port: int = 7777):
        """
        Initializes a new instance of the server object

        Args:
            address (str): The IP address (or FQDN) of the dedicated server
            key (str): The API key to be used when accessing the server. Can be either the API key + payload, or the bare key.
            port (int, optional): The port the server is running on. Defaults to 7777.

        Raises:
            ConnectionError: Raised if
        """
        # Initialize logger
        self.logger = logging.getLogger("Server-Connect")
        logging.basicConfig(
            filename="serverConnect.log", encoding="utf-8", level=logging.DEBUG
        )

        if address is None:
            self.logger.info("No address given! Creating empty object")
            # TODO: Initialize params
            self.address = None
            return
        else:
            # Do initial connection, verify token
            self.login(address, token, port)

    def __str__(self) -> str:
        """Returns a human-readable string representation of the current object

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

    def login(self, address: str = None, token: str = None, port: int = 7777):
        self.address = "https://" + address + ":" + str(port) + "/api/v1"
        self.logger.info(f"Connecting to {self.address}...")
        # Split token into payload and key
        if len(token.split(".")) > 1:
            # payload + token
            token = token.split(".")
            tokenPayload = token[0]
            key = str(token[0]) + "." + str(token[1])
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
        # else, assume just key in token
        else:
            key = token

        self.headers = {"Encoding": "utf-8", "Authorization": f"Bearer {key}"}
        initResponse = self._postJSONRequest(
            self.headers,
            payload={"function": "VerifyAuthenticationToken"},
        )
        # Check if connection successful
        if initResponse == 523:
            # Unable to contact server at given address
            raise ConnectionError(f"Connection to {address} failed with no response!")
        # TODO: Raise different exception based on HTTP code
        if initResponse.status_code == requests.codes.no_content:
            self.logger.info("Connection Successful")
            self.logger.info(f"Authenticated with {authLevel} privilege")
            self.loggedIn = True
            return 204  # No Content
        else:
            self.logger.error(
                f"Connection to {address} failed with status {initResponse.status_code}!\
                    \nResponse: {initResponse.content}"
            )
            raise ConnectionError(
                f"Connection to {address} failed with status {initResponse.status_code}!"
            )

    def _postJSONRequest(self, headers: dict, payload: dict) -> requests.Response:
        """
        Sends an HTTP request to the server using a JSON formatted payload

        Args:
            headers (dict): A dict of standard HTTP headers to be included with the request
            payload (dict): A dict of dedicated server function data

        Returns:
            requests.Response: _description_
        """
        if not self.loggedIn:
            self.logger.error("")
        try:
            response = requests.post(
                self.address, headers=headers, json=payload, verify=False
            )
            return response
        except requests.exceptions.ConnectionError:
            self.logger.critical("Unable to contact server")
            # CloudFlare HTTP response 523: Origin Unreachable
            return 523

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

    def queryServerState(self):
        response = self._postJSONRequest(self.headers, {"function": "QueryServerState"})

        self.logger.info(f"Received {response.status_code} response from server")
        content = json.loads(response.content)["data"]["serverGameState"]
        phase = content["gamePhase"]
        if phase in self.prettyPhase:
            content["gamePhase"] = self.prettyPhase[phase]

        self.logger.info(content)
        return content


if __name__ == "__main__":
    # server = SatisfactoryServerAdmin(
    #     "192.168.1.17",
    #     "ewoJInBsIjogIkFQSVRva2VuIgp9.8A737E3138243B97CE20CA13BC1A8075EDFBF1FFA88EA7797A4AB9BF2683495B47286F2188769B50B43ECC6E0C8210F18F8A85F649EED540230AFAA685958711",
    #     7777,
    # )
    server = SatisfactoryServerAdmin()
    server.login(
        "192.168.1.17",
        "ewoJInBsIjogIkFQSVRva2VuIgp9.8A737E3138243B97CE20CA13BC1A8075EDFBF1FFA88EA7797A4AB9BF2683495B47286F2188769B50B43ECC6E0C8210F18F8A85F649EED540230AFAA685958711",
        7777,
    )
    # server.login(
    #     "a",
    #     "a",
    #     7777,
    # )
    print(server.queryServerState())
    print(str(server))

# server = SatisfactoryServer(
#     "192.168.1.17",
#     "ewoJInBsIjogIkFQSVRva2VuIgp9.8A737E3138243B97CE20CA13BC1A8075EDFBF1FFA88EA7797A4AB9BF2683495B47286F2188769B50B43ECC6E0C8210F18F8A85F649EED540230AFAA685958711",
# )
