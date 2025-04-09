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

    # Window Update Loop
    # TODO: Check which tab is active, update accordingly
    while True:  # TODO: Use LW Query to determine if update is needed
        if server.loggedIn:
            server.pollServerState()
            serverName.text = server.serverName
            sessionName.text = server.sessionName
            updateStatusDisp(window, server.serverState)
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
    statusRun = window.dom.get_element("#run")
    statusStart = window.dom.get_element("#start")
    statusPause = window.dom.get_element("#pause")
    statusStop = window.dom.get_element("#stop")

    statusRun.classes.append("d-none")
    statusStart.classes.append("d-none")
    statusPause.classes.append("d-none")
    statusStop.classes.append("d-none")
    match newState:
        case "idle":
            statusStop.classes.remove("d-none")
        case "loading":
            statusStart.classes.remove("d-none")
        case "playing":
            if server.paused:
                statusPause.classes.remove("d-none")
            else:
                statusRun.classes.remove("d-none")


def updateSettingsDisp() -> None:
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
        "Satisfactory Server Administrator V0.0.4", "./index.html", js_api=server
    )
    webview.start(main, window, debug=False)  # Blocking after start
