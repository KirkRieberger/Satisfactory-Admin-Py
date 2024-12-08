from time import sleep
import webview
from SatisfactoryServerAdmin import SatisfactoryServerAdmin


def loop(window: webview.Window):
    # Setup visual fields
    serverName = window.dom.get_element("#server")
    sessionName = window.dom.get_element("#session")
    statusRun = window.dom.get_element("#run")
    statusStart = window.dom.get_element("#start")
    statusPause = window.dom.get_element("#pause")
    statusStop = window.dom.get_element("#stop")
    phase = window.dom.get_element("#phase")
    tier = window.dom.get_element("#tier")
    schematic = window.dom.get_element("#schem")
    playerCount = window.dom.get_element("#curPlayers")
    maxCount = window.dom.get_element("#maxPlayers")
    tickRate = window.dom.get_element("#ticks")

    # Window Update Loop
    while True:  # TODO: Use LW Query to determine if update is needed
        if server.loggedIn:
            server.pollServerState()
            serverName.text = server.serverName
            phase.text = server.gamePhase
            sessionName.text = server.sessionName
            tier.text = server.tier
            schematic.text = server.schematic
            playerCount.text = server.numPlayers
            maxCount.text = server.maxPlayers
            tickRate.text = server.tickRate
            match server.serverState:
                case "idle":
                    statusRun.classes.append("d-none")
                    statusStart.classes.append("d-none")
                    statusPause.classes.append("d-none")
                    statusStop.classes.remove("d-none")
                case "loading":
                    statusRun.classes.append("d-none")
                    statusStart.classes.remove("d-none")
                    statusPause.classes.append("d-none")
                    statusStop.classes.append("d-none")
                case "playing":
                    if server.paused:
                        statusRun.classes.append("d-none")
                        statusStart.classes.append("d-none")
                        statusPause.classes.remove("d-none")
                        statusStop.classes.append("d-none")
                    else:
                        statusRun.classes.remove("d-none")
                        statusStart.classes.append("d-none")
                        statusPause.classes.append("d-none")
                        statusStop.classes.append("d-none")

            sleep(10)
        else:
            sleep(1)


server = SatisfactoryServerAdmin()
window = webview.create_window(
    "Satisfactory Server Administrator V0.0.1", "./index.html", js_api=server
)
webview.start(loop, window, debug=False)  # Blocking after start
