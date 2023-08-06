from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtGui import QAction, QDesktopServices
from PyQt6.QtCore import QUrl

from FanTeX.pdfviewer import FTPDFViewer
from FanTeX.fsviewer import FTFSViewer
from FanTeX.editor import FTEditor

import FanTeX


class FTMainWindow(QMainWindow):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.setWindowTitle(f"FanTeX {FanTeX.__version__}")
        self.resize(width, height)
        self.setCentralWidget(QWidget(self))
        self.project_dir = ""
        self.fsviewer = FTFSViewer(parent=self)
        self.pdfviewer = FTPDFViewer(parent=self)
        self.editor = FTEditor(parent=self)
        self.layout = QHBoxLayout()
        self.centralWidget().setLayout(self.layout)
        self.layout.addWidget(self.fsviewer)
        self.layout.addWidget(self.pdfviewer)
        self.layout.addWidget(self.editor)
        self._create_actions()
        self._create_menu()
        self._connect_actions()

    def _create_actions(self) -> None:
        # File menu actions
        self.newAction = QAction("&New project", self)
        self.openProjAction = QAction("&Open project", self)
        self.openPDFAction = QAction("Open &PDF", self)
        self.quitAction = QAction("&Quit", self)
        # Help menu actions
        self.helpAction = QAction("About FanTeX", self)
        self.helpQtAction = QAction("About Qt", self)

    def _connect_actions(self) -> None:
        # File menu actions
        self.newAction.triggered.connect(self.new_project)
        self.openProjAction.triggered.connect(self.open_project)
        self.quitAction.triggered.connect(self.close)
        self.openPDFAction.triggered.connect(self.openPDF)
        # Help menu actions
        self.helpAction.triggered.connect(self.open_homepage)
        self.helpQtAction.triggered.connect(
            lambda: QMessageBox.aboutQt(self, "About Qt")
        )

    def new_project(self):
        self.open_project()

    def open_project(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.FileMode.Directory)
        if dlg.exec():
            dirs = dlg.selectedFiles()
            if len(dirs) == 1:
                self.project_dir = dirs.pop()
                self.fsviewer.set_project_dir(self.project_dir)

    def open_homepage(self):
        url = QUrl(FanTeX.__homepage__)
        QDesktopServices.openUrl(url)

    def _create_menu(self) -> None:
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")
        # File menu actions
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openProjAction)
        fileMenu.addAction(self.openPDFAction)
        fileMenu.addAction(self.quitAction)
        # Help menu actions
        helpMenu.addAction(self.helpAction)
        helpMenu.addAction(self.helpQtAction)

    def openPDF(self) -> None:
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
        dlg.setNameFilter("PDF (*.pdf)")
        if dlg.exec():
            files = dlg.selectedFiles()
            if len(files) == 1:
                pdf_file = files.pop()
                self.pdfviewer.load_file(pdf_file)
                self.pdfviewer.show_pdf()
