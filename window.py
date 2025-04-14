from time import sleep
import webview
from SatisfactoryServerAdmin import SatisfactoryServerAdmin


class WindowController:

    def __init__(self, server):
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
        settingsrestartTime = self.window.dom.get_element("#restartTime")
        settingsNetworkQuality = self.window.dom.get_element("#networkQuality")
        print(self.window.dom.get_element("#status"))
        pass


if __name__ == "__main__":
    server = SatisfactoryServerAdmin()
    windowController = WindowController(server)
    window = webview.create_window(
        "Satisfactory Server Administrator V0.0.154", "./index.html", js_api=server
    )
    window.expose(windowController.updateSettingsDisp)
    webview.start(windowController.main, window,
                  debug=False)  # Blocking after start
