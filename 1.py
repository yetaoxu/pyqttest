from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import hashlib

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.filewidget = filelabel(self)
        self.setCentralWidget(self.filewidget)
        self.statusBar()
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.filewidget.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.resize(450, 250)
        self.center()
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowTitle('File dialog')
        self.show()

class filelabel(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.initfilelabel()

    def initfilelabel(self):
        self.filenamelabel = QLabel('filename')
        font = QFont()
        font.setWeight(75)
        font.setPointSize(20)
        self.filenamelabel.setFont(font)
        self.pathlabel = QLabel('path')
        self.pathlabel.setFont(font)
        self.FilePathEdit = QLineEdit()
        self.FilePathEdit.setReadOnly(True)
        self.FileMd5Edit = QLineEdit()
        self.FileMd5Edit.setReadOnly(True)

        self.qfl = QFormLayout()
        self.qfl.addWidget(self.filenamelabel)
        self.qfl.addWidget(self.pathlabel)
        self.qfl.addRow(self.filenamelabel, self.FilePathEdit)
        self.qfl.addRow(self.pathlabel, self.FileMd5Edit)
        self.FilePathEdit.setPlaceholderText("请选择文件路径")
        self.FileMd5Edit.setPlaceholderText("将显示文件的md5")
        self.qfl.setHorizontalSpacing(30)
        self.setLayout(self.qfl)

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/User/xuyetao/Document')
        if fname[0]:
            f = open(fname[0], 'rb')
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            f.close()
            md5 = str(hash_code).lower()
            self.FilePathEdit.setText(fname[0])
            self.FileMd5Edit.setText(md5)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())



