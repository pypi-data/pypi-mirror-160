import os
from pathlib import Path

from PyQt5.QtWidgets import (
    QListWidgetItem,
    QListWidget,
    QWidget,
    QHBoxLayout,
    QLabel,
    QCheckBox,
)


class FileItem(QListWidgetItem):
    """
    A class used to create custom QListWidgetItems.

    Attributes
    ----------
    file_path: str
        a path to the file.
    Methods
    -------
    name() -> str
        returns the basename of the file.
    """

    def __init__(self, file_path: str, parent: QListWidget, hidden: bool = False):
        QListWidgetItem.__init__(self, parent)
        self._file_path = file_path
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        if hidden:
            self.label = QLabel("Image " + str(parent.row(self) + 1))
        else:
            path: str = self.get_name()
            if len(path) > 28:
                path = path[0:27] + "..."
            self.label = QLabel(path)
        self.layout.addWidget(self.label, stretch=19)
        self.check = QCheckBox()
        self.check.setCheckState(False)
        self.check.setCheckable(not hidden)
        self.layout.addWidget(self.check, stretch=1)
        self.layout.addStretch()
        self.layout.setContentsMargins(2, 2, 0, 5)
        self.label.setStyleSheet(
            """
                QLabel{
                    border: 0px solid; 
                }
        """
        )
        self.widget.setLayout(self.layout)
        self.setSizeHint(self.widget.sizeHint())
        if parent is not None:
            parent.setItemWidget(self, self.widget)

    def get_name(self):
        """Return basename"""
        return Path(self._file_path).stem

    @property
    def file_path(self) -> str:
        return self._file_path

    def highlight(self):
        """highlight item"""
        self.label.setStyleSheet(
            """QLabel{
                            font-weight: bold;
                            text-decoration: underline;
                        }"""
        )

    def unhighlight(self):
        """unhighlight item"""
        self.label.setStyleSheet("""QLabel{}""")

    def __hash__(self):
        return hash(self._file_path)

    def __eq__(self, other):
        """Compares two ListItems file_path attributes"""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._file_path == other._file_path
