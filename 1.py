from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import hashlib

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.FileWidget = FileLabel(self)
        self.setCentralWidget(self.FileWidget)
        self.statusBar()
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.FileWidget.ShowDialog)

        MenuBar = self.menuBar()
        FileMenu = MenuBar.addMenu('&File')
        FileMenu.addAction(openFile)
        self.resize(450, 250)
        self.Center()
    def Center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowTitle('File dialog')
        self.show()

class FileLabel(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.initFileLabel()

    def initFileLabel(self):
        self.FileNameLabel = QLabel('filename')
        self.PathLabel = QLabel('path')
        self.FilePathEdit = QLineEdit()
        self.FilePathEdit.setReadOnly(True)
        self.FileMd5Edit = QLineEdit()
        self.FileMd5Edit.setReadOnly(True)

        self.FilePathEdit.setMinimumWidth(250)
        self.FileMd5Edit.setMinimumWidth(250)

        self.spa1 = QSpacerItem(50, 50)
        self.spa2 = QSpacerItem(50, 50)
        self.qfl = QFormLayout()

        self.hlayout = QHBoxLayout()
        self.hlayout.addItem(self.spa1)
        self.hlayout.addLayout(self.qfl)
        self.hlayout.addItem(self.spa2)
        self.qfl.addWidget(self.FileNameLabel)
        self.qfl.addWidget(self.PathLabel)
        self.qfl.addRow(self.FileNameLabel, self.FilePathEdit)
        self.qfl.addRow(self.PathLabel, self.FileMd5Edit)
        self.FilePathEdit.setPlaceholderText("请选择文件路径")
        self.FileMd5Edit.setPlaceholderText("将显示文件的md5")
        self.qfl.setHorizontalSpacing(8)
        self.setLayout(self.hlayout)

    def ShowDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/User/xuyetao/Document')
        if fname[0]:
            f = open(fname[0], 'rb')
            Md5Obj = hashlib.md5()
            Md5Obj.update(f.read())
            HashCode = Md5Obj.hexdigest()
            f.close()
            Md5 = str(HashCode).lower()
            self.FilePathEdit.setText(fname[0])
            self.FileMd5Edit.setText(Md5)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())



