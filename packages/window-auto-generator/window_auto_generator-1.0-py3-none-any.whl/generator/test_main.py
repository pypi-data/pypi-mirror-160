import unittest
import sys
from PyQt5.QtWidgets import QApplication
from main import ToolWindow, ToolConf, ReqProto, Button


class TestStringMethods(unittest.TestCase):
    def test_gen_window(self):
        app = QApplication(sys.argv)
        ToolWindow(ToolConf(
            name="my window",
            desc="my window desc",
            buttons=[
                Button("test", "desc", ReqProto("http://127.0.0.1:8000/hello?user=1", "GET", None)),
            ]
        ))
        sys.exit(app.exec_())


if __name__ == '__main__':
    unittest.main()
