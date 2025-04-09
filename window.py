from time import sleep
import webview
from SatisfactoryServerAdmin import SatisfactoryServerAdmin


def main(window: webview.Window):
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
            serverName.text = server.serverName
            sessionName.text = server.sessionName
            updateStatusDisp(window, server.serverState)
            # Update dashboard
            # TODO: Factor into bespoke function
            if updateSettings:
                updateSettingsDisp(window)
            phase.text = server.gamePhase
            tier.text = server.tier
            schematic.text = server.schematic
            playerCount.text = server.numPlayers
            maxCount.text = server.maxPlayers
            tickRate.text = server.tickRate
            changeList.text = server.clientVersion

            sleep(int(updateRate.value))
        else:
            sleep(1)


def updateStatusDisp(window: webview.Window, newState: str) -> None:
    status = window.dom.get_element("#status")

    match newState:
        case "idle":
            status.classes = ["bi", "bi-stop-circle-fill", "text-danger"]
        case "loading":
            status.classes = ["bi", "bi-skip-end-circle-fill", "text-warning"]
        case "playing":
            if server.paused:
                status.classes = ["bi", "bi-pause-circle-fill", "text-warning"]
            else:
                status.classes = ["bi", "bi-play-circle-fill", "text-success"]


def updateSettingsDisp(window: webview.Window) -> None:
    # Standard Settings
    settingsAutoPause = window.dom.get_element("#autoPause")
    settingsAutoSaveDC = window.dom.get_element("#autoSaveOnDC")
    settingsTelemetry = window.dom.get_element("#telemetry")
    settingsSaveInterval = window.dom.get_element("#saveInterval")
    settingsrestartTime = window.dom.get_element("#restartTime")
    settingsNetworkQuality = window.dom.get_element("#networkQuality")
    print(settingsAutoPause.text)
    pass


if __name__ == "__main__":
    server = SatisfactoryServerAdmin()
    window = webview.create_window(
        "Satisfactory Server Administrator V0.0.154", "./index.html", js_api=server
    )
    webview.start(main, window, debug=True)  # Blocking after start
