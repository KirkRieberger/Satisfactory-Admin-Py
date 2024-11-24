from time import sleep
import webview
from SatisfactoryServerAdmin import SatisfactoryServerAdmin


def test(window):
    while True:
        if server.loggedIn:
            state = server.queryServerState()
            window.dom.get_element("#phase").text = state["gamePhase"]
        else:
            sleep(10)


server = SatisfactoryServerAdmin()
window = webview.create_window("Test", "./index.html", js_api=server)
webview.start(test, window, debug=True)
