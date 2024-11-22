import webview
from SatisfactoryServerAdmin import SatisfactoryServerAdmin


def test(window):
    window.evaluate_js(
        """
        """
    )


server = SatisfactoryServerAdmin()
window = webview.create_window("Test", "./index.html")
webview.start(test, window)
