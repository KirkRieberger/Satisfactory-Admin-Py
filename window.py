from time import sleep
import webview
from SatisfactoryServerAdmin import SatisfactoryServerAdmin


def loop(window: webview.Window):
    # Setup visual fields
    serverName = window.dom.get_element("#server")
    sessionName = window.dom.get_element("#session")
    phase = window.dom.get_element("#phase")
    tier = window.dom.get_element("#tier")
    schematic = window.dom.get_element("#schem")
    playerCount = window.dom.get_element("#curPlayers")
    maxCount = window.dom.get_element("#maxPlayers")
    tickRate = window.dom.get_element("#ticks")

    # Window Update Loop
    while True:  # TODO: Use LW Query to determine if update is needed
        if server.loggedIn:
            server.pollServerState(window, server.serverState)
            serverName.text = server.serverName
            phase.text = server.gamePhase
            sessionName.text = server.sessionName
            tier.text = server.tier
            schematic.text = server.schematic
            playerCount.text = server.numPlayers
            maxCount.text = server.maxPlayers
            tickRate.text = server.tickRate

            sleep(10)
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


if __name__ == "__main__":
    server = SatisfactoryServerAdmin()
    window = webview.create_window(
        "Satisfactory Server Administrator V0.0.1", "./index.html", js_api=server
    )
    webview.start(loop, window, debug=False)  # Blocking after start
