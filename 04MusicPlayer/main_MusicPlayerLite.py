import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QFileDialog, 
                             QHeaderView, QAbstractItemView, QLabel)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Qt

from Ui_playerLite import Ui_Form


def format_ms(ms):
    """毫秒 -> MM:SS"""
    s = ms // 1000
    return f"{s // 60:02d}:{s % 60:02d}"


class MusicPlayerLite(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(self.width(), self.height())
        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        self.model = QStandardItemModel(0, 2, self)
        self.model.setHorizontalHeaderLabels(["歌名"])
        self.musicTable.setModel(self.model)
        
        self.setup_ui_extras()
        self.init_connections()

    def setup_ui_extras(self):
        header = self.musicTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.musicTable.setColumnHidden(1, True)
        self.musicTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.musicTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.audio_output.setVolume(0.5)

        # 进度条下方时间标签
        self.timeLabel = QLabel("00:00 / 00:00")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setStyleSheet("color: #666; font-size: 11px;")
        # 插入到进度条下方
        self.verticalLayout.insertWidget(1, self.timeLabel)

    def init_connections(self):
        self.listBtn.clicked.connect(self.import_music)
        self.playBtn.clicked.connect(self.toggle_playback)
        self.preBtn.clicked.connect(lambda: self.switch_song(-1))
        self.nextBtn.clicked.connect(lambda: self.switch_song(1))
        
        self.musicTable.doubleClicked.connect(self.play_selected)
        
        self.volumeSlider.valueChanged.connect(lambda v: self.audio_output.setVolume(v / 100))
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        self.progressSlider.sliderMoved.connect(self.player.setPosition)

        # 播放结束自动下一首
        self.player.mediaStatusChanged.connect(self.on_media_status)


    def import_music(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择音频", "", "音频 (*.mp3 *.flac *.wav *.ogg *.m4a)")
        if files:
            for f in files:
                name = os.path.splitext(os.path.basename(f))[0]

                self.model.appendRow([
                    QStandardItem(name),
                    QStandardItem(f),
                ])

    def toggle_playback(self):
        state = self.player.playbackState()
        if state == QMediaPlayer.PlayingState:
            self.player.pause()
            self.playBtn.setText("播放")
        elif state == QMediaPlayer.PausedState:
            # 检查选中的歌曲是否与当前播放的不同
            idx = self.musicTable.currentIndex()
            if idx.isValid():
                selected_path = self.model.item(idx.row(), 1).text()
                current_path = self.player.source().toLocalFile()
                if selected_path != current_path:
                    self.play_selected()
                    return
            self.player.play()
            self.playBtn.setText("暂停")
        else:
            self.play_selected()

    def play_selected(self, index=None):
        if index is None:
            index = self.musicTable.currentIndex()
        if not index.isValid():
            if self.model.rowCount() > 0:
                index = self.model.index(0, 0)
                self.musicTable.setCurrentIndex(index)
            else:
                return
        row = index.row()
        self.musicTable.setCurrentIndex(self.model.index(row, 0))
        path = self.model.item(row, 1).text()
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()
        self.playBtn.setText("暂停")

    def on_duration_changed(self, duration):
        self.progressSlider.setRange(0, duration)
        self.timeLabel.setText(f"00:00 / {format_ms(duration)}")

    def on_position_changed(self, pos):
        if not self.progressSlider.isSliderDown():
            self.progressSlider.setValue(pos)
        dur = self.player.duration()
        self.timeLabel.setText(f"{format_ms(pos)} / {format_ms(dur)}")

    def on_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.switch_song(1)

    def switch_song(self, step):
        total_rows = self.model.rowCount()
        if total_rows == 0: return
        current_row = self.musicTable.currentIndex().row()
        next_row = (max(0, current_row) + step) % total_rows
        self.musicTable.setCurrentIndex(self.model.index(next_row, 0))
        self.play_selected()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MusicPlayerLite()
    window.show()
    sys.exit(app.exec())