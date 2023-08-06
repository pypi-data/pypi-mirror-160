import requests
import re
from typing import List, Dict

from PyQt5.QtWidgets import (QWidget, QTextBrowser, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow)


class ReqProto:
    def __init__(self, url: str, method: str, data: Dict[str, str]):
        if not re.match(r'^https?:/{2}\w.+$', url):
            raise TypeError(f'{url} invalid')
        self.url = url
        self.method = method
        self.data = data

    def do_req(self) -> str:
        if self.method == "GET":
            return requests.get(url=self.url).text
        elif self.method == "POST":
            return requests.post(url=self.url, data=self.data).text


class Button(QPushButton):
    def __init__(self, name: str, desc: str, req_proto: ReqProto):
        super().__init__(name)
        self.name = name
        self.desc = desc
        self.req_proto = req_proto
        self.window = None

    def on_click(self):
        c = f"{self.name}, {self.desc}"
        if not self.window:
            return
        ret = self.req_proto.do_req()
        self.window.text_browser.setText(f"{c}: {ret}")


class ToolConf:
    def __init__(self, name: str, desc: str, buttons: List[Button]):
        self.name = name
        self.desc = desc
        self.buttons = buttons


class ToolWindow(QMainWindow):
    def __init__(self, conf: ToolConf):
        super().__init__()
        self.text_browser = None
        self.page_layout = QVBoxLayout()
        self.conf = conf
        self.tool_name = self.conf.name
        self.tool_desc = self.conf.desc
        self.buttons = self.conf.buttons
        self.init_window()

    def init_window(self):
        self.setToolTip(self.tool_desc)
        self.setWindowTitle(self.tool_name)
        self.init_text_browser()
        self.init_buttons()
        self.show()

    def init_text_browser(self):
        browser_layout = QVBoxLayout()
        self.page_layout.addLayout(browser_layout)
        tb = QTextBrowser()
        tb.setAcceptRichText(True)
        tb.setOpenExternalLinks(True)
        self.text_browser = tb
        self.page_layout.addWidget(tb)

    def init_buttons(self):
        button_layout = QHBoxLayout()
        self.page_layout.addLayout(button_layout)
        for btn in self.buttons:
            button = Button(name=btn.name, desc=btn.desc, req_proto=btn.req_proto)
            button.clicked.connect(button.on_click)
            button.window = self
            button_layout.addWidget(button)
        widget = QWidget()
        widget.setLayout(self.page_layout)
        self.setCentralWidget(widget)
