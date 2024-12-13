import numpy
import requests
import socket
import select
import json
import base64
import logging
from random import randint
from sys import exit as sys_ex

# Possible to connect with payload+token and just token

__author__ = "Kirk Rieberger"
__version__ = "0.0.1"
__date__ = "Nov 21, 2024"


class SatisfactoryServerAdmin:
    """Contains a reference to a running Satisfactory Dedicated Server. Provides certain management functions"""

    # Static class variables
    prettyPhase = {
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_1.GP_Project_Assembly_Phase_1'": "Distribution Platform",
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_2.GP_Project_Assembly_Phase_2'": "Construction Dock",
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_3.GP_Project_Assembly_Phase_3'": "Main Body",
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_4.GP_Project_Assembly_Phase_4'": "Propulsion",
        "/Script/FactoryGame.FGGamePhase'/Game/FactoryGame/GamePhases/GP_Project_Assembly_Phase_5.GP_Project_Assembly_Phase_5'": "Assembly",
    }

    prettySchematic = {
        # Tier 0 - Onboarding
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_0-1.Schematic_0-1_C'": "HUB Upgrade 1",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_0-2.Schematic_0-2_C'": "HUB Upgrade 2",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_0-3.Schematic_0-3_C'": "HUB Upgrade 3",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_0-4.Schematic_0-4_C'": "HUB Upgrade 4",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_0-5.Schematic_0-5_C'": "HUB Upgrade 5",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_0-6.Schematic_0-6_C'": "HUB Upgrade 6",
        # Phase 0 - Tier 1
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_1-1.Schematic_1-1_C'": "Base Building",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_1-2.Schematic_1-2_C'": "Logistics",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_1-3.Schematic_1-3_C'": "Field Research",
        # Phase 0 - Tier 2
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_2-1.Schematic_2-1_C'": "Part Assembly",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_2-2.Schematic_2-2_C'": "Obstacle Clearing",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_2-3.Schematic_2-3_C'": "Jump Pads",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_2-4.Schematic_2-4_C'": "Resource Sink Bonus Program",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_2-5.Schematic_2-5_C'": "Logistics Mk.2",
        # Phase 1 - Tier 3 - Distribution Platform
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_3-1.Schematic_3-1_C'": "Coal Power",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_3-2.Schematic_3-2_C'": "Vehicular Transport",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_3-3.Schematic_3-3_C'": "Basic Steel Production",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_3-4.Schematic_3-4_C'": "Enhanced Asset Security",
        # Phase 1 - Tier 4 - Distribution Platform
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_4-1.Schematic_4-1_C'": "FICSIT Blueprints",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_4-2.Schematic_4-2_C'": "Logistics Mk.3",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_4-3.Schematic_4-3_C'": "Advanced Steel Production",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_4-4.Schematic_4-4_C'": "Expanded Power Infrastructure",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_4-5.Schematic_4-5_C'": "Hypertubes",
        # Phase 2 - Tier 5 - Construction Dock
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_5-1.Schematic_5-1_C'": "Jetpack",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_5-2.Schematic_5-2_C'": "Oil Processing",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_5-3.Schematic_5-3_C'": "Logistics Mk.4",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_5-4.Schematic_5-4_C'": "Fluid Packaging",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_5-5.Schematic_5-5_C'": "Petroleum Power",
        # Phase 2 - Tier 6 - Construction Dock
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_6-1.Schematic_6-1_C'": "Industrial Manufacturing",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_6-2.Schematic_6-2_C'": "Monorail Train Technology",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_6-3.Schematic_6-3_C'": "Railway Signaling",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_6-4.Schematic_6-4_C'": "Pipeline Engineering Mk.2",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_6-5.Schematic_6-5_C'": "FICSIT Blueprints Mk.2",
        # Phase 3 - Tier 7 - Main Body
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_7-1.Schematic_7-1_C'": "Bauxite Refinement",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_7-2.Schematic_7-2_C'": "Hoverpack",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_7-3.Schematic_7-3_C'": "Logistics Mk.5",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_7-4.Schematic_7-4_C'": "Hazmat Suit",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_7-5.Schematic_7-5_C'": "Control System Development",
        # Phase 3 - Tier 8 - Main Body
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_8-1.Schematic_8-1_C'": "Aeronautical Engineering",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_8-2.Schematic_8-2_C'": "Nuclear Power",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_8-3.Schematic_8-3_C'": "Advanced Aluminum Production",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_8-4.Schematic_8-4_C'": "Leading-edge Production",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_8-5.Schematic_8-5_C'": "Particle Enrichment",
        # Phase 4 - Tier 9 - Propulsion
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_9-1.Schematic_9-1_C'": "Matter Conversion",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_9-2.Schematic_9-2_C'": "Quantum Encoding",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_9-3.Schematic_9-3_C'": "Ficsit Blueprints Mk.3",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_9-4.Schematic_9-4_C'": "Spatial Energy Regulation",
        "/Script/Engine.BlueprintGeneratedClass'/Game/FactoryGame/Schematics/Progression/Schematic_9-5.Schematic_9-5_C'": "Peak Efficiency",
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

    def __init__(self, ip: str = None, token: str = None, port: int = 7777):
        """
        Initializes a new instance of the server object

        Args:
            ip (str): The IP address (or FQDN) of the dedicated server
            token (str): The API key to be used when accessing the server. Can be either the API key + payload, or the bare key.
            port (int, optional): The port the server is running on. Defaults to 7777.
        """

        # Instance variables
        #  Class state
        self.address = None
        self.ip = None
        self.port = None
        self.headers = None
        self.loggedIn = False
        self.subStates = {}

        #  Displayed values
        #   Header
        self.serverName = None
        self.sessionName = None
        self.serverState = None
        #   Game Info
        self.gamePhase = None  # Number
        self.tier = None  # String
        self.schematic = None  # String
        #   Server State
        self.numPlayers = None
        self.maxPlayers = None
        self.tickRate = None
        self.autoSessionName = None
        self.paused = None
        self.clientVersion = None
        #   Save Info
        self.duration = None

        # Initialize logger
        self.logger = logging.getLogger("Server-Connect")
        logging.basicConfig(
            filename="serverConnect.log", encoding="utf-8", level=logging.DEBUG
        )

        if ip is None:
            self.logger.info("No address given! Creating empty object")
            return
        else:
            # Do initial connection, verify token
            self.login(ip, token, port)

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

    def login(self, ip: str = None, token: str = None, port: str = "7777") -> int:
        """
        Attempts to perform an API key login with the specified server.

        Args:
            ip (str, optional): The IP address (or FQDN) of the dedicated server. Defaults to None.
            token (str, optional): The API key to be used when accessing the server. Can be either the API key + payload, or the bare key. Defaults to None.
            port (int, optional): The port the server is running on. Defaults to 7777.

        Raises:
            TimeoutError: If the connection to the specified address times out
            ConnectionError: If another error occurs during token validation

        Returns:
            int: HTTP status code 204 if successful
        """
        self.ip = ip
        self.port = port
        self.address = "https://" + ip + ":" + str(port) + "/api/v1"
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
                sys_ex()  # TODO: Shouldn't exit. Should raise exception for UI to handle

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
            raise TimeoutError(f"Connection to {self.address} failed with no response!")
        # TODO: Raise different exception based on HTTP code
        if initResponse.status_code == requests.codes.no_content:
            self.logger.info("Connection Successful")
            self.logger.info(f"Authenticated with {authLevel} privilege")
            self.loggedIn = True
            return 204  # No Content
        else:
            self.logger.error(
                f"Connection to {self.address} failed with status {initResponse.status_code}!\
                    \nResponse: {initResponse.content}"
            )
            raise ConnectionError(
                f"Connection to {self.address} failed with status {initResponse.status_code}!"
            )

    def _postJSONRequest(self, headers: dict, payload: dict) -> requests.Response:
        """
        Sends an HTTP request to the server using a JSON formatted payload

        Args:
            headers (dict): A dict of standard HTTP headers to be included with the request
            payload (dict): A dict of dedicated server function data

        Returns:
            requests.Response: The HTTP response body if successful
            int: Cloudflare HTTP response 523 - Destination Unreachable on timeout
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

    def _LightweightQuery(self) -> list:
        """
        Determines the server changelist by performing a lightweight UDP query of the connected server

        Raises:
            TimeoutError: Non-fatal error if response isn't received from server in time

        Returns:
            list: Bitmask of changed states: [Server State, Server Options, Advanced Game Settings, Save Sessions]
        """
        serverStates = {0: "offline", 1: "idle", 2: "loading", 3: "playing"}
        subStateStatus = [0, 0, 0, 0]  # Returned value
        # Server State, Server Options, AGS, Save Sessions

        # Query identifier
        payload = numpy.uint64(randint(0, 2**64 - 1))

        message = b"".join(
            [
                numpy.uint16(0xF6D5),  # protocolMagic
                numpy.uint8(0),  # messageType
                numpy.uint8(1),  # protocolVersion
                payload,  # payload
                numpy.uint8(0x1),  # terminator
            ]
        )

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", 7777))
        sock.sendto(message, (self.ip, self.port))

        try:
            # Timeout of ~0.15 - 0.2 for virtual machine/host connection
            ready = select.select([sock], [], [], 0.1)
            if ready[0]:
                data, addr = sock.recvfrom(1024)
                self.logger.debug(f"Message Received from {addr}: {data}")
            else:
                raise TimeoutError("UDP response timed out")
        except TimeoutError:
            # UDP response timed out, assume no change
            # Don't need to close socket because "finally" is respected
            self.logger.warning("UDP response timed out. Skipping this cycle")
            return subStateStatus
        finally:
            sock.close()

        # Parse response

        respMagic = int.from_bytes(
            data[0:2], byteorder="little"
        )  # Should be 0xf6d5  -  Unbound local
        if respMagic != 0xF6D5:
            self.logger.error("Invalid lightweight query magic number!")
            # Update self if necessary

        respType = int.from_bytes(data[2:3])  # Should be 0x01
        if respType != 0x01:
            self.logger.error("Invalid lightweight query response type!")

        respVer = int.from_bytes(data[3:4])  # Should be 0x01
        if respVer != 0x01:
            self.logger.error("Invalid lightweight query response version!")

        # Current time in Unreal Engine game ticks. Not terribly useful
        # respCookie = hex(int.from_bytes(data[4:12], byteorder="little"))

        respState = int.from_bytes(data[12:13])
        if respState not in range(0, 4):
            self.logger.error("Invalid lightweight query server state!")
        else:
            self.serverState = serverStates[respState]

        # Server version - matches game version cl#______
        self.clientVersion = int.from_bytes(data[13:17], byteorder="little")

        respFlags = int.from_bytes(data[17:25], byteorder="little")
        if (respFlags & 0x8000000000000000) != 0:  # Bitmask for 64th (modded flag) bit
            # Server is modded
            self.logger.warning(
                "Server appears modded! Some features might not work as expected!"
            )

        numStates = int.from_bytes(data[25:26])
        # Substate is a counter incremented each time a relevant setting is changed

        # respStates = data[26 : 26 + (3 * numStates)]
        i = 26  # Base offset of state array
        while i < (26 + numStates * 3):
            stateId = int.from_bytes(
                data[i : i + 1]
            )  # Single byte - Order not necessary
            stateData = int.from_bytes(data[i + 1 : i + 4], byteorder="little")

            if stateId in self.subStates:
                if stateData != self.subStates[stateId]:
                    # Settings changed
                    subStateStatus[stateId] = 1
            else:
                # Initial run
                self.subStates[stateId] = stateData
                subStateStatus[stateId] = 1

            i += 3

        respNameLen = int.from_bytes(
            data[26 + (3 * numStates) : 26 + (3 * numStates) + 2],
            byteorder="little",
        )
        self.serverName = data[
            26 + (3 * numStates) + 2 : 26 + (3 * numStates) + 2 + respNameLen
        ].decode("utf-8")

        # Terminator 0x01

        return subStateStatus

    def passwordlessLogin(self, headers: dict) -> tuple:
        """
        Performs a passwordless login to the server. Grants User level access.
        Should not be used for third-party app logins

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

    def _queryServerState(self) -> None:
        """Query the server's state endpoint, and update class members"""
        # Get response
        response = self._postJSONRequest(self.headers, {"function": "QueryServerState"})
        # TODO: Check if valid response
        self.logger.info(f"Received {response.status_code} response from server")
        content = json.loads(response.content)["data"]["serverGameState"]

        # Update instance variables
        self.sessionName = content["activeSessionName"]
        self.numPlayers = content["numConnectedPlayers"]
        self.maxPlayers = content["playerLimit"]
        self.tier = content["techTier"]

        # Prettify phase and schematic
        self.schematic = content["activeSchematic"]
        if self.schematic in self.prettySchematic:
            self.schematic = self.prettySchematic[self.schematic]

        self.gamePhase = content["gamePhase"]
        if self.gamePhase in self.prettyPhase:
            self.gamePhase = self.prettyPhase[self.gamePhase]

        self.duration = content["totalGameDuration"]
        self.tickRate = round(content["averageTickRate"], 2)
        self.paused = content["isGamePaused"]
        self.autoSessionName = content["autoLoadSessionName"]
        self.logger.info(content)
        return content  # Temp

    def _queryServerOptions(self) -> None:
        # TODO:
        pass

    def _queryAdvancedGameSettings(self) -> None:
        # TODO:
        pass

    def pollServerState(self) -> None:
        """Poll the lightweight query API to determine if a call to the HTTP
        API is required, then poll the required APIs"""
        changeList = self._LightweightQuery()
        if changeList[0]:
            # Server State
            self._queryServerState()
        if changeList[1]:
            # Server Options
            self._queryServerOptions()
        if changeList[2]:
            # AGS
            self._queryAdvancedGameSettings()
        if changeList[3]:
            # Enumerate Sessions
            pass
        # Determine if update is necessary
        # Query parts that need updating


if __name__ == "__main__":
    server = SatisfactoryServerAdmin()
    server.login("IP", "Key", 7777)
    server.pollServerState()
    # print(server.queryServerState())
    # server._LightweightQuery()
