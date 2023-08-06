from PyQt6.QtWidgets import QWidget, QTreeView, QVBoxLayout
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir


class FTFSViewer(QWidget):
    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.fsmodel = QFileSystemModel(self)
        self.fsmodel.setRootPath(QDir.homePath())
        self.treeView = QTreeView(self)
        self.treeView.setModel(self.fsmodel)

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)

    def set_project_dir(self, path: str) -> None:
        """Update the filesystem TreeView to show the given directory path

        Args:
            path (str): directory path
        """
        self.treeView.setRootIndex(self.fsmodel.index(path))
