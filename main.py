from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog
from PyQt5.QtCore import Qt, QUrl

from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

import sys
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowIcon(QIcon("logo.ico"))
        self.setWindowTitle("PyPlayer")
        self.setGeometry(350,100,700,500)
        p = self.palette()
        p.setColor(QPalette.Window,Qt.blue)
        self.setPalette(p)
        self.create_player()

    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        self.openBtn = QPushButton("Open Video")
        self.openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)


        self.slider = QSlider(Qt.Horizontal)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)

        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


    def open_file(self):
        filename,_ = QFileDialog.getOpenFileName(self,"Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()




app = QApplication(sys.argv)
window  = Window()
window.show()
sys.exit(app.exec_())

