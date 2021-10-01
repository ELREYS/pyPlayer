from PyQt5 import QtMultimedia
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtNetwork import QNetworkRequest
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog, \
    QLabel
from PyQt5.QtCore import Qt, QUrl

from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

import sys
from datetime import datetime

from PyQt5.uic.properties import QtCore


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

        self.durationLbl = QLabel("00:00")
        self.durationLbl.setStyleSheet("color:white;")



        self.openBtn = QPushButton("Open Video")
        self.openBtn.clicked.connect(self.open_urlfile)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)


        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.durationLbl)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)

        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)
        vbox.addLayout(hbox)

        #Connect VideoOutput
        self.mediaPlayer.setVideoOutput(videowidget)

        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)




    def open_file(self):
        filename,_ = QFileDialog.getOpenFileName(self,"Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def open_urlfile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        with open(filename, 'rb') as stream:
            self._data = stream.read()
            self._buffer.setData(self._data)
            self._buffer.open(QtCore.QIODevice.ReadOnly)
            self.player.setMedia(
                QtMultimedia.QMediaContent(), self._buffer)
            self.player.play()

        if url != '':
            self.mediaPlayer.setMedia(QMediaContent((QUrl(url))))
            self.playBtn.setEnabled(True)



    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    def mediastate_changed(self,state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self,position):
        print(f"Position:{position}")
        _position = self.mediaPlayer.position()/ 1000
        self.durationLbl.setText(self.calculate_duration(_position))
        self.slider.setValue(position)

    def calculate_duration(self,duration):
        s = duration
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        print
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))


    def duration_changed(self,duration):
        print(f"Duration:{duration}")
        _duration = self.mediaPlayer.duration() / 1000
        self.durationLbl.setText(self.calculate_duration(_duration))
        self.slider.setRange(0,duration)


    def set_position(self,position):
        self.mediaPlayer.setPosition(position)





app = QApplication(sys.argv)
window  = Window()
window.show()
sys.exit(app.exec_())

