import webview
from SatisfactoryServerAdmin import SatisfactoryServerAdmin


def test(window):
    window.evaluate_js(
        """
        """
    )


window = webview.create_window("Test", "./index.html", js_api=SatisfactoryServerAdmin())
webview.start(test, window, debug=False)
