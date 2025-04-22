import numpy
import requests
import socket
import select
import json
import base64
import logging
import SatisfactoryLuT
from random import randint
from sys import exit as sys_ex

__author__ = "Kirk Rieberger"
__version__ = "0.0.170"
__date__ = "Apr 18, 2025"


class SatisfactoryServerAdmin:
    """Contains a reference to a running Satisfactory Dedicated
    Server. Provides certain management functions
    """

    # Static class variables
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
        # Requires InitialAdmin privilege level, which can only be
        #   acquired by attempting passwordless login while the server
        #   does not have an Admin Password set. Requires new server
        #   name and admin password.
        "RenameServer",
        # Returns nothing on success.
        # Requires new server name
        "SetClientPassword",
        # Returns nothing on success.
        # Requires new client password IN PLAIN TEXT
        "SetAdminPassword",
        # Returns nothing on success.
        # Requires new admin password IN PLAIN TEXT and new token to
        #   use
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
        # Returns array of sessions on server and index of loaded
        #   session.
        "LoadGame",
        # Returns nothing on success.
        # Requires name of save file to load and AGS enable bool
        "UploadSaveGame",
        # Requires name of save to upload, immediate load bool,
        #   AGS bool, and save file as multipart form request
        "DownloadSaveGame",
        # Returns save file.
        # Requires name of save file to download
    ]

    def __init__(self, ip: str = None, token: str = None, port: int = 7777,
                 validateSSL: bool = True):
        """
        Initializes a new instance of the server object

        Args:
            ip (str): The IP address (or FQDN) of the dedicated server

            token (str): The API key to be used when accessing the
            server.

            port (int, optional): The port the server is running on.
            Defaults to 7777.
        """

        # Instance variables
        self.validateSSL = validateSSL
        #  Class state
        self.address = None
        self.ip = None
        self.token = None
        self.port = None
        self.headers = None
        self.loggedIn = False
        self.subStates = {}  # substate ID: state changelist
        self.needsRestart = False  # Pending options

        #  Dashboard
        #   Header
        self.serverName = None  # ✔
        self.sessionName = None  # ✔
        self.serverState = None  # Lightweight Query ✔
        self.paused = None  # HTTPS Query ✔
        #   Game Info
        self.gamePhase = None  # Number ✔
        self.tier = None  # String ✔
        self.schematic = None  # String ✔
        self.duration = None  #
        #   Server State
        self.numPlayers = None  # ✔
        self.maxPlayers = None  # ✔
        self.tickRate = None  # ✔
        self.autoSessionName = None  #

        # Settings
        #  Server Options
        self.autoPause = None  #
        self.saveOnDisconnect = None  #
        self.autosaveInterval = None  # In seconds
        self.restartTime = None  # In minutes
        self.sendGameplayData = None  #
        self.networkQuality = None  #
        #  AGS
        self.creativeMode = None  #
        self.noPower = None  #
        self.disableArachnids = None  #
        self.noUnlock = None  #
        self.allTiers = None  #
        self.setPhase = None  #
        self.unlockAllSchematics = None  #
        self.unlockAllAlts = None  #
        self.unlockAllShop = None  #
        self.noBuildCost = None  #
        self.godMode = None  #
        self.flightMode = None  #

        # Persistent
        self.clientVersion = None  # Lightweight Query ✔

        # Initialize logger
        self.logger = logging.getLogger("Server-Connect")
        logging.basicConfig(
            filename="serverConnect.log",
            encoding="utf-8",
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)s:%(filename)s:%(message)s",
            datefmt="%Y/%m/%d - %H:%M:%S")

        if ip is None:
            self.logger.info("No address given! Creating empty object")
            return
        else:
            # Do initial connection, verify token
            self.login(ip, token, port)

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the current
        object

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
        return f"SatisfactoryServer('{self.address}', '{self.token}')"

    def login(self, ip: str = None, token: str = None, port: str = "7777") -> int:
        """
        Attempts to perform an API key login with the specified server.

        Args:
            ip (str, optional): The IP address (or FQDN) of the
            dedicated server. Defaults to None.

            token (str, optional): The API key to be used when
            accessing the server. Defaults to None.

            port (int, optional): The port the server is running on.
            Defaults to 7777.

        Raises:
            TimeoutError: If the connection to the specified address
            times out
            ConnectionError: If another error occurs during token
            validation

        Returns:
            int: HTTP status code 204 if successful
        """
        # TODO: Verify input before attempting connect
        if not port.isnumeric():
            raise ValueError("Provided port is not numeric")
        if ip is None:
            # Use ip already stored
            pass
        else:
            self.ip = ip

        self.port = int(port)

        if token is None:
            # Use token already stored
            pass
        else:
            self.token = token

        if (ip is None) or (token is None):
            # Cannot perform interactive login without both address and
            #   token. Return
            return

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
                # TODO: Shouldn't exit. Should raise exception for UI to handle
                sys_ex()

            try:
                authLevel = json.loads(decodedPayload)["pl"]
            except KeyError:
                self.logger.fatal(
                    "Provided token payload is invalid. Did you provide a\
                        Satisfactory Server API Token?"
                )
                # TODO: Shouldn't exit. Should raise exception for UI to handle
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
            raise TimeoutError(
                f"Connection to {self.address} failed with no response!")
        # TODO: Raise different exception based on HTTP code
        if initResponse.status_code == requests.codes.no_content:
            self.logger.info("Connection Successful")
            self.logger.info(f"Authenticated with {authLevel} privilege")
            self.loggedIn = True
            return 204  # No Content
        else:
            self.logger.error(
                f"Connection to {self.address} failed with status \
                {initResponse.status_code}! \nResponse: {initResponse.content}"
            )
            raise ConnectionError(
                f"Connection to {self.address} failed with status {initResponse.status_code}!"
            )

    def _postJSONRequest(self, headers: dict, payload: dict) -> requests.Response:
        """
        Sends an HTTP request to the server using a JSON formatted
        payload

        Args:
            headers (dict): A dict of standard HTTP headers to be
                included with the request
            payload (dict): A dict of dedicated server function data

        Returns:
            requests.Response: The HTTP response body if successful

            int: Cloudflare HTTP response 523 - Destination Unreachable
                on timeout
        """
        # TODO: Move login check to each function, not POST
        if not self.loggedIn:
            self.logger.error("")  # TODO: Can't error. used for login
        try:
            response = requests.post(
                self.address, headers=headers, json=payload, verify=self.validateSSL
            )
            return response
        except requests.exceptions.SSLError as e:
            self.logger.error(
                f"Connection to {self.address} failed with error 495: SSL\
                    Certificate error!")
            self.logger.error(e.args[0].reason)
            return 495
        except requests.exceptions.ConnectionError:
            self.logger.critical("Unable to contact server")
            # CloudFlare HTTP response 523: Origin Unreachable
            return 523

    def _LightweightQuery(self) -> list:
        """
        Determines the server changelist by performing a lightweight
        UDP query of the connected server

        Raises:
            TimeoutError: Non-fatal error if response isn't received
            from server in time

        Returns:
            list: Bitmask of changed states: [Server State, Server
            Options, Advanced Game Settings, Save Sessions]
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
            # Assume corrupt data. Skip this update
            return [0, 0, 0, 0]

        respType = int.from_bytes(data[2:3])  # Should be 0x01
        if respType != 0x01:
            self.logger.error("Invalid lightweight query response type!")
            # Assume corrupt data. Skip this update
            return [0, 0, 0, 0]

        respVer = int.from_bytes(data[3:4])  # Should be 0x01
        if respVer != 0x01:
            self.logger.error("Invalid lightweight query response version!")
            # Assume corrupt data. Skip this update
            return [0, 0, 0, 0]

        # Current time in Unreal Engine game ticks. Not terribly useful
        # respCookie = hex(int.from_bytes(data[4:12], byteorder="little"))

        respState = int.from_bytes(data[12:13])
        if respState not in range(0, 4):
            self.logger.error("Invalid lightweight query server state!")
            # Assume corrupt data. Skip this update
            return [0, 0, 0, 0]
        else:
            self.serverState = serverStates[respState]

        # Server version - matches game version cl#______
        self.clientVersion = int.from_bytes(data[13:17], byteorder="little")

        respFlags = int.from_bytes(data[17:25], byteorder="little")
        # Bitmask for 64th (modded flag) bit
        if (respFlags & 0x8000000000000000) != 0:
            # Server is modded
            self.logger.warning(
                "Server appears modded! Some features might not work as expected!"
            )

        numStates = int.from_bytes(data[25:26])
        # Substate is a counter incremented each time a relevant
        #   setting is changed

        # respStates = data[26 : 26 + (3 * numStates)]
        i = 26  # Base offset of state array
        while i < (26 + numStates * 3):
            stateId = int.from_bytes(
                data[i: i + 1]
            )  # Single byte - Order not necessary
            stateData = int.from_bytes(data[i + 1: i + 4], byteorder="little")

            if stateId in self.subStates:
                if stateData != self.subStates[stateId]:
                    # Settings changed
                    subStateStatus[stateId] = 1
                else:
                    subStateStatus[stateId] = 0
            else:
                # Initial run
                self.subStates[stateId] = stateData
                subStateStatus[stateId] = 1

            i += 3

        respNameLen = int.from_bytes(
            data[26 + (3 * numStates): 26 + (3 * numStates) + 2],
            byteorder="little",
        )
        self.serverName = data[
            26 + (3 * numStates) + 2: 26 + (3 * numStates) + 2 + respNameLen
        ].decode("utf-8")

        terminator = data[26 + (3 * numStates) + 2 + respNameLen]
        if terminator != 0x01:
            # Assume corrupt data. Skip this update
            return [0, 0, 0, 0]

        return subStateStatus

    # Basic Functionality

    def _passwordlessLogin(self, ip: str, port: str = "7777") -> bool:
        """
        Performs a passwordless login to the server. Grants InitialAdmin
        access. Used to claim server.

        Args:
            ip (str): The IP address (or FQDN) of the dedicated server.
            port (str, optional): The port the server is running on.
                Defaults to "7777".

        Returns:
            bool: Whether the InitialAdmin login attempt was successful
        """
        self.address = "https://" + ip + ":" + str(port) + "/api/v1"
        self.logger.info(f"Connecting to {self.address}...")
        self.headers = {"Encoding": "utf-8",
                        "Content-Type": "application/json"}
        payload = {
            "function": "PasswordlessLogin",
            "data": {"MinimumPrivilegeLevel": "InitialAdmin"},
        }
        initResponse = self._postJSONRequest(self.headers, payload=payload)

        if initResponse == 495:
            # SSL Error
            return False
        elif initResponse == 523:
            # Other connection error
            return False

        data = initResponse.json()
        if "errorCode" in data:
            self.logger.error(data["errorCode"])
            return False
        else:
            token = data["data"]["authenticationToken"]
            self.token = token
            self.headers.update({"Authorization": f"Bearer {token}"})
            return True

    def _queryServerState(self) -> None:
        """
        Query the server's state endpoint, and update class members
        """
        # Get response
        response = self._postJSONRequest(
            self.headers, {"function": "QueryServerState"})
        # TODO: Check if valid response
        self.logger.info(
            f"Received {response.status_code} response from server")
        content = json.loads(response.content)["data"]["serverGameState"]

        # Update instance variables
        self.sessionName = content["activeSessionName"]
        self.numPlayers = content["numConnectedPlayers"]
        self.maxPlayers = content["playerLimit"]
        self.tier = content["techTier"]

        # Prettify phase and schematic
        self.schematic = SatisfactoryLuT.getSchematic(
            content["activeSchematic"])

        self.gamePhase = SatisfactoryLuT.getPhase(content["gamePhase"])

        self.duration = content["totalGameDuration"]
        self.tickRate = round(content["averageTickRate"], 2)
        self.paused = content["isGamePaused"]
        self.autoSessionName = content["autoLoadSessionName"]
        self.logger.info(content)

    # Modify Server Options

    def _queryServerOptions(self) -> None:
        """
        Query the server's options endpoint, and update class members
        """
        response = self._postJSONRequest(
            self.headers, {"function": "GetServerOptions"})
        # TODO: Check if valid response
        self.logger.info(
            f"Received {response.status_code} response from server")
        currentOptions = json.loads(response.content)["data"]["serverOptions"]
        pendingOptions = json.loads(response.content)[
            "data"]["pendingServerOptions"]
        if pendingOptions:
            self.needsRestart = True

        self.autoPause = currentOptions["FG.DSAutoPause"]
        self.saveOnDisconnect = currentOptions["FG.DSAutoSaveOnDisconnect"]
        self.autosaveInterval = currentOptions["FG.AutosaveInterval"]
        self.restartTime = currentOptions["FG.ServerRestartTimeSlot"]
        if currentOptions["FG.SendGameplayData"] == "True":
            self.sendGameplayData = True
        else:
            self.sendGameplayData = False
        self.networkQuality = currentOptions["FG.NetworkQuality"]

    def _applyServerOptions(self) -> None:
        pass

    def _queryAdvancedGameSettings(self) -> None:
        # TODO:
        """
        Query the server's advanced game settings endpoint, and update class members
        """
        response = self._postJSONRequest(
            self.headers, {"function": "GetAdvancedGameSettings"}
        )
        # TODO: Check if valid response
        self.logger.info(
            f"Received {response.status_code} response from server")
        ags = json.loads(response.content)["data"]["advancedGameSettings"]
        self.creativeMode = json.loads(response.content)[
            "data"]["creativeModeEnabled"]
        self.noPower = ags["FG.GameRules.NoPower"]
        self.disableArachnids = ags["FG.GameRules.DisableArachnidCreatures"]
        self.noUnlock = ags["FG.GameRules.NoUnlockCost"]
        self.allTiers = ags["FG.GameRules.GiveAllTiers"]
        self.setPhase = ags["FG.GameRules.SetGamePhase"]
        self.unlockAllSchematics = ags["FG.GameRules.UnlockAllResearchSchematics"]
        self.unlockAllAlts = ags["FG.GameRules.UnlockInstantAltRecipes"]
        self.unlockAllShop = ags["FG.GameRules.UnlockAllResourceSinkSchematics"]
        self.noBuildCost = ags["FG.PlayerRules.NoBuildCost"]
        self.godMode = ags["FG.PlayerRules.GodMode"]
        self.flightMode = ags["FG.PlayerRules.FlightMode"]

    def _applyAdvancedGameSettings(self) -> None:
        pass

    def _renameServer(self, newName: str) -> None:
        if not newName:
            self.logger.warning("No new server name provided!")
            # TODO: Notify user newName is empty
        payload = {"function": "RenameServer", "data": {"ServerName": newName}}
        response = self._postJSONRequest(self.headers, payload)
        if response.status_code != 204:
            self.logger.error(
                f"Connection to {self.address} failed with \
                              status {response.status_code}! \nResponse: \
                              {response.content}"
            )
        # TODO: Notify user of success

    # New Server Tasks

    def claimServerInit(self, adr: str = None, port: str = "7777") -> int:
        """
        TODO:
        Begins the server claiming process. Determines if a server is
        already claimed.

        Args:
            adr (str, optional): _description_. Defaults to None.
            port (str, optional): _description_. Defaults to "7777".

        Returns:
            bool: _description_
        """
        # Requires "Initial Admin" privilege
        # Received when attempting passwordless login with no admin pswd set
        if adr is None:
            self.logger.error("claimServerInit - Invalid address provided!")
            return -1
        if self._passwordlessLogin(adr, port):
            # Do not give token here. This is initialAdmin token
            return 0  # TODO: Confirm to UI server is unclaimed
            # UI to continue flow at claimServerSetup
        else:
            # Login Failed, assume server claimed
            return 1

    def claimServerSetup(self, newName: str, admPassword: str) -> None:
        # TODO: Get ServerName and AdminPassword from UI
        # TODO: [OPTIONAL] Set user password
        payload = {
            "function": "ClaimServer",
            "data": {
                "ServerName": newName,
                "AdminPassword": admPassword,
            },
        }

        response = self._postJSONRequest(self.headers, payload)
        # TODO: Extract new auth token. Provide to user
        # Update token to drop initial admin

        # Gives "administrator" token, not API token.
        # TODO: Request API token
        self.token = response.json()["data"]["authenticationToken"]
        return self.token

    def _setClientPassword(self) -> None:
        pass

    def _setAdminPassword(self) -> None:
        pass

    # Save/Session Management

    def _setAutoLoadSessionName(self) -> None:
        pass

    def _createNewGame(self) -> None:
        pass

    def _saveGame(self) -> None:
        pass

    def _deleteSaveFile(self) -> None:
        pass

    def _enumerateSessions(self) -> None:
        pass

    def _loadGame(self) -> None:
        pass

    def _uploadSaveGame(self) -> None:
        pass

    def _downloadSaveGame(self) -> None:
        pass

    # Miscellaneous

    def _runCommand(self) -> None:
        pass

    def _serverShutdown(self) -> None:
        pass

    # User Interface

    def pollServerState(self) -> None:
        """
        Poll the lightweight query API to determine if a call to the
        HTTP API is required, then poll the required APIs
        """
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
    # All Transient
    server = SatisfactoryServerAdmin()
    server.claimServerInit("192.168.1.133")
