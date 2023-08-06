import os
import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from FanTeX.mainwindow import FTMainWindow


class FanTeXApplication:
    """The application class that holds all UI components together"""

    def __init__(self, *args, **kwargs):
        self.app = QApplication(*args, **kwargs)
        # Global font setting
        self.app.setFont(QFont("Arial"))
        self.app.font().setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        # Let the window be 85% of the screen's size and centered
        scrn_geom = self.app.primaryScreen().availableGeometry()
        w = int(0.5 * scrn_geom.width())
        h = int(0.85 * scrn_geom.height())
        self.win = FTMainWindow(width=w, height=h)
        self.win.geometry().moveCenter(scrn_geom.center())

    def run(self):
        """Display main window and start running"""
        self.win.showMaximized()
        self.app.exec()
        self.win.close()


def run():
    """Entry point for starting the application"""
    # Prevent the window from being blurry if Windows scales
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    FanTeXApplication(sys.argv).run()


if __name__ == "__main__":
    run()
