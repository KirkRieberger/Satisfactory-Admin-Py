from time import sleep
import webview
from SatisfactoryServerAdmin import SatisfactoryServerAdmin
from SatisfactoryServerAdmin import __version__ as version


class WindowController:

    def __init__(self, server: SatisfactoryServerAdmin):
        self.server = server

    def main(self, window: webview.Window):
        self.window = window
        # Setup visual fields
        #  Header
        serverName = window.dom.get_element("#server")
        sessionName = window.dom.get_element("#session")
        #  Dashboard
        #   Game Info
        phase = window.dom.get_element("#phase")
        tier = window.dom.get_element("#tier")
        schematic = window.dom.get_element("#schem")
        #   Server State
        playerCount = window.dom.get_element("#curPlayers")
        maxCount = window.dom.get_element("#maxPlayers")
        tickRate = window.dom.get_element("#ticks")
        #  Persistent
        changeList = window.dom.get_element("#version")
        updateRate = window.dom.get_element("#updateRate")

        # Tracking variables
        updateSettings = None

        # Window Update Loop
        # TODO: Check which tab is active, update accordingly
        while True:  # TODO: Use LW Query to determine if update is needed
            if server.loggedIn:
                server.pollServerState()
                serverName.text = self.server.serverName
                sessionName.text = self.server.sessionName
                self.updateStatusDisp(self.server.serverState)
                # Update dashboard
                # TODO: Factor into bespoke function
                if updateSettings:
                    self.updateSettingsDisp(window)
                phase.text = self.server.gamePhase
                tier.text = self.server.tier
                schematic.text = self.server.schematic
                playerCount.text = self.server.numPlayers
                maxCount.text = self.server.maxPlayers
                tickRate.text = self.server.tickRate
                changeList.text = self.server.clientVersion

                sleep(int(updateRate.value))
            else:
                sleep(1)

    def updateStatusDisp(self, newState: str) -> None:
        status = self.window.dom.get_element("#status")

        match newState:
            case "idle":
                status.classes = ["bi", "bi-stop-circle-fill", "text-danger"]
            case "loading":
                status.classes = [
                    "bi", "bi-skip-end-circle-fill", "text-warning"]
            case "playing":
                if self.server.paused:
                    status.classes = [
                        "bi", "bi-pause-circle-fill", "text-warning"]
                else:
                    status.classes = [
                        "bi", "bi-play-circle-fill", "text-success"]

    def updateSettingsDisp(self) -> None:
        # Standard Settings
        settingsAutoPause = self.window.dom.get_element("#autoPause")
        settingsAutoSaveDC = self.window.dom.get_element("#autoSaveOnDC")
        settingsTelemetry = self.window.dom.get_element("#telemetry")
        settingsSaveInterval = self.window.dom.get_element("#saveInterval")
        settingsRestartTime = self.window.dom.get_element("#restartTime")
        settingsNetworkQuality = self.window.dom.get_element("#networkQuality")

        if self.server.autoPause:
            settingsAutoPause.attributes["checked"] = ""
        else:
            settingsAutoPause.attributes["checked"] = None

        if self.server.saveOnDisconnect:
            settingsAutoSaveDC.attributes["checked"] = ""
        else:
            settingsAutoSaveDC.attributes["checked"] = None

        if self.server.sendGameplayData:
            settingsTelemetry.attributes["checked"] = ""
        else:
            settingsTelemetry.attributes["checked"] = None

        settingsSaveInterval.value = int(float(self.server.autosaveInterval))
        settingsRestartTime.value = int(float(self.server.restartTime))

        if self.server.networkQuality == 0:
            settingsNetworkQuality.value = 0
        elif self.server.networkQuality == 1:
            settingsNetworkQuality.value = 1
        elif self.server.networkQuality == 2:
            settingsNetworkQuality.value = 2
        elif self.server.networkQuality == 3:
            settingsNetworkQuality.value = 3


if __name__ == "__main__":
    server = SatisfactoryServerAdmin(validateSSL=False)
    windowController = WindowController(server)
    window = webview.create_window(
        f"Satisfactory Server Administrator V{version}", "./index.html",
        js_api=server, min_size=(1024, 800)
    )
    window.expose(windowController.updateSettingsDisp)
    webview.start(windowController.main, window,
                  debug=True)  # Blocking after start
    print("closed")
