import pathlib

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from PyQt6.QtWidgets import QWidget, QTextBrowser, QVBoxLayout, QTabWidget
from PyQt6.QtGui import QFont


class TexHighlighter:
    def __init__(self) -> None:
        self.lexer = get_lexer_by_name("tex", stripall=True)
        self.change_style()

    def change_style(self, style="xcode"):
        self.style = style
        self.formatter = HtmlFormatter(full=True, noclasses=True, style=self.style)

    def highlight(self, code: str):
        return highlight(code, self.lexer, self.formatter)


class FTEditor(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.texEditor = self._create_tex_editor()
        self.tex_highlighter = TexHighlighter()
        self.addTab(self.texEditor, "TeX")
        self.load_tex()

    def _create_tex_editor(self) -> QWidget:
        texEditor = QWidget()
        self.texBrowser = QTextBrowser()
        font = QFont()
        font.setPointSizeF(11)
        self.texBrowser.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.texBrowser)
        texEditor.setLayout(layout)
        return texEditor

    def load_tex(self) -> None:
        FanTeX_tex = pathlib.Path(__file__).joinpath("../FanTeX.tex").resolve()
        if pathlib.Path.exists(FanTeX_tex):
            html_to_display = self.tex_highlight(open(FanTeX_tex).read())
            self.texBrowser.setHtml(html_to_display)

    def tex_highlight(self, code: str) -> str:
        return self.tex_highlighter.highlight(code)
