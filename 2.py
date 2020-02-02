import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
class wi(QWidget):
    def __init__(self):
        super().__init__()
        self.initfilelabel()

    def initfilelabel(self):
        self.UrlInfo = QLineEdit()
        self.UrlInfo.setReadOnly(True)
        self.DirInfo = QLineEdit()
        self.DirInfo.setReadOnly(True)

        self.qfl = QFormLayout()
        self.qfl.addRow('urlInfo', self.UrlInfo)
        self.qfl.addRow('dirInfo', self.DirInfo)
        self.UrlInfo.setPlaceholderText("download url")
        self.DirInfo.setPlaceholderText("save directory")
        self.qfl.setHorizontalSpacing(30)
        self.qfl.FieldGrowthPolicy(1)
        self.setLayout(self.qfl)

class mainwin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar()
        self.openFile = QAction(QIcon('download.png'), 'Download', self)
        self.openFile.setShortcut('Ctrl+O')
        self.openFile.setStatusTip('Download a File')
        self.openFile.triggered.connect(self.openwin2)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.openFile)

        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('File Info')
        self.center()

    def openwin2(self):
        w2 = win2()
        w2.urlInfoSignal.connect(self.getDialogSignal1)
        w2.exec_()

    def getDialogSignal1(self, info1, info2):
        wid = wi()
        self.setCentralWidget(wid)
        wid.setLayout(wid.qfl)
        wid.UrlInfo.setText(info1)
        wid.DirInfo.setText(info2)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

class win2(QDialog):
    urlInfoSignal = pyqtSignal(str, str)
    pathInfoSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initwidget()

    def initwidget(self):
        self.resize(400, 150)
        self.center()
        self.cancelbtn = QPushButton('cancel', self)
        self.cancelbtn.setEnabled(True)
        self.cancelbtn.clicked.connect(self.close)
        self.urledit = QLineEdit(self)
        self.confirmbtn = QPushButton('confirm', self)

        self.progressBar = QProgressBar(self, minimumWidth=250)
        self.progressBar.setValue(0)

        self.confirmbtn.setEnabled(True)
        self.confirmbtn.clicked.connect(self.sendEditContent)
        self.confirmbtn.clicked.connect(self.on_pushButton_clicked)

        self.directoryedit = QLineEdit(self)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.cancelbtn)
        self.hlayout.addWidget(self.confirmbtn)

        self.qfl = QFormLayout()
        self.qfl.addRow('url', self.urledit)
        self.qfl.addRow('directory', self.directoryedit)
        self.qfl.addRow('progress bar', self.progressBar)
        self.qfl.addRow(self.hlayout)

        self.urledit.setPlaceholderText('input url')
        self.directoryedit.setPlaceholderText('save folder')
        self.qfl.setHorizontalSpacing(30)
        self.setLayout(self.qfl)

    def sendEditContent(self):
        urlcontent = self.urledit.text()
        downloadcontent = self.directoryedit.text()
        self.urlInfoSignal.emit(urlcontent, downloadcontent)

    # 下载部分参考博文 https://blog.csdn.net/qq_20265805/article/details/88899066

    def on_pushButton_clicked(self):
        the_url = self.urledit.text()
        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = self.directoryedit.text()
        the_fileobj = open(the_filepath, 'wb')
        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()

    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "Info", "success ！")
            return

    def center(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)
                self.fileobj.write(chunk)
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))
            self.fileobj.close()
            self.exit(0)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = mainwin()
    m.show()
    sys.exit(app.exec_())