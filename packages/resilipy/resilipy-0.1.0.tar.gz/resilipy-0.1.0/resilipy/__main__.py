from resilipy.scripts.buider import Builder
from resilipy.scripts.preprocessor import Preprocessor
from resilipy.scripts.labeler import Labeler

import webbrowser
import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication


class ResiliPy(QMainWindow):
    def __init__(self):
        super().__init__()
        dirname = os.path.dirname(__file__)
        ui = os.path.join(dirname, "ui/resilipy.ui")
        uic.loadUi(ui, self)
        self.builder = None
        self.preprocessor = None
        self.labeler = None

        self.buttonBuilder.pressed.connect(self.start_builder)
        self.buttonPreprocessor.pressed.connect(self.start_preprocessor)
        self.buttonLabeler.pressed.connect(self.start_labeler)

        self.buttonGuide.pressed.connect(self.open_guide)
        self.buttonGithub.pressed.connect(self.open_github)

    def start_builder(self):
        self.builder = Builder()
        self.close()
        self.builder.show()

    def start_preprocessor(self):
        self.preprocessor = Preprocessor()
        self.close()
        self.preprocessor.show()

    def start_labeler(self):
        self.labeler = Labeler()
        self.close()
        self.labeler.show()

    def open_guide(self):
        webbrowser.open("https://gitlab.rlp.net/vdietric/resilipy/-/wikis/home")

    def open_github(self):
        webbrowser.open("https://gitlab.rlp.net/vdietric/resilipy")


app = QApplication(sys.argv)
resilipy = ResiliPy()
resilipy.show()

app.exec()
