import webview
from webview.window import Window

import server


def test(window: Window):
    window.evaluate_js("alert('Works!');")


with open("index.html", "rt") as page:
    page = page.read()
window = webview.create_window(title="Test", html=page)
webview.start(test, window)
