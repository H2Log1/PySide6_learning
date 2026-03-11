import sys
import os
import re
from PySide6.QtWidgets import (QApplication, QWidget, QTableWidgetItem, 
                             QHeaderView, QFileDialog, QLabel, QVBoxLayout, 
                             QListWidget, QListWidgetItem)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QPixmap, QImage

from Ui_player import Ui_Form

class MyMusicPlayer(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(self.width(), self.height())
        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        self.lyric_data = [] 
        
        self.init_ui_logic()
        self.init_connections()

    def init_ui_logic(self):
        # 侧边栏初始化
        self.setList.addItems(["音乐封面", "显示歌词"])
        # 连接到自定义的切换逻辑
        self.setList.currentRowChanged.connect(self.handle_view_switch)
        
        # 封面布局
        self.cover_layout = QVBoxLayout(self.page)
        self.cover_label = QLabel("等待播放...")
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_layout.addWidget(self.cover_label)

        # 歌词列表布局
        self.lyric_layout = QVBoxLayout(self.page_2)
        # self.lyric_label = QLabel("歌词显示区")
        self.lyric_list = QListWidget()
        self.lyric_list.setStyleSheet("""
            QListWidget { background: transparent; border: none; color: #888; font-size: 18px; outline: none; }
            QListWidget::item { padding: 12px; border: none; }
            QListWidget::item:selected { color: #00d4ff; font-size: 22px; font-weight: bold; background: transparent; }
        """)
        self.lyric_layout.addWidget(self.lyric_list)

        # 播放列表配置
        self.musicList.setColumnCount(3)
        self.musicList.setHorizontalHeaderLabels(["歌名", "类型"])
        self.musicList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.musicList.setColumnHidden(2, True)

        self.radioSlider.setRange(0, 100)
        self.radioSlider.setValue(50)
        self.audio_output.setVolume(0.5)

    def handle_view_switch(self, index):
        self.mainStacked.setCurrentIndex(index)
        
        # 判断显隐：歌词页1隐藏，封面页0显示
        if index == 1:
            self.musicList.setVisible(False)
        else:
            self.musicList.setVisible(True)

    def init_connections(self):
        self.listBtn.clicked.connect(self.import_music)
        self.playBtn.clicked.connect(self.handle_play_press)
        self.pauseBtn.clicked.connect(self.player.pause)
        self.nextBtn.clicked.connect(lambda: self.switch_track(1))
        self.formerBtn.clicked.connect(lambda: self.switch_track(-1))
        
        self.musicList.itemDoubleClicked.connect(self.play_selected_row)
        
        self.radioSlider.valueChanged.connect(lambda v: self.audio_output.setVolume(v / 100))
        
        self.player.durationChanged.connect(self.update_duration_range)
        self.player.positionChanged.connect(self.sync_ui_with_postition)
        self.progressSlider.sliderMoved.connect(self.player.setPosition)

    def import_music(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择音频", "", "音频 (*.mp3 *.flac *.wav)")
        if files:
            for f in files:
                row = self.musicList.rowCount()
                self.musicList.insertRow(row)
                self.musicList.setItem(row, 0, QTableWidgetItem(os.path.basename(f)))
                self.musicList.setItem(row, 1, QTableWidgetItem(os.path.splitext(f)[1].upper()))
                self.musicList.setItem(row, 2, QTableWidgetItem(f))

    def update_duration_range(self, duration):
        if duration > 0:
            self.progressSlider.setRange(0, duration)

    def sync_ui_with_postition(self, pos):
        if not self.progressSlider.isSliderDown():
            self.progressSlider.setValue(pos)
        
        if self.lyric_data:
            idx = 0
            for i, (t, txt) in enumerate(self.lyric_data):
                if pos >= t: idx = i
                else: break
            self.lyric_list.setCurrentRow(idx)
            self.lyric_list.scrollToItem(self.lyric_list.currentItem(), QListWidget.PositionAtCenter)

    def handle_play_press(self):
        if self.player.playbackState() == QMediaPlayer.PausedState:
            self.player.play()
        else:
            curr_row = self.musicList.currentRow()
            if curr_row != -1: self.load_and_play(curr_row)

    def play_selected_row(self, item):
        self.load_and_play(item.row())

    def load_and_play(self, row):
        file_path = self.musicList.item(row, 2).text()
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.update_metadata(file_path)
        self.player.play()
        self.musicList.selectRow(row)

    def update_metadata(self, path):
        from mutagen import File
        try:
            audio = File(path)
            # 封面
            data = None
            if audio.tags:
                if 'APIC:' in audio.tags: data = audio.tags['APIC:'].data
                elif hasattr(audio, 'pictures') and audio.pictures: data = audio.pictures[0].data
            
            if data:
                img = QImage.fromData(data)
                pix = QPixmap.fromImage(img).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.cover_label.setPixmap(pix)
            else:
                self.cover_label.setText("无内嵌封面")

            lyrics_text = ""
            if audio.tags:
                uslt = [v for k, v in audio.tags.items() if k.startswith('USLT')]
                if uslt: lyrics_text = uslt[0].text
                elif 'LYRICS' in audio.tags: lyrics_text = audio.tags['LYRICS'][0]

            if not lyrics_text:
                lrc = os.path.splitext(path)[0] + ".lrc"
                if os.path.exists(lrc):
                    with open(lrc, 'r', encoding='utf-8') as f: lyrics_text = f.read()

            self.parse_lyrics(lyrics_text)
        except:
            pass

    def parse_lyrics(self, text):
        self.lyric_data = []
        self.lyric_list.clear()
        if not text:
            self.lyric_list.addItem("未发现歌词")
            return

        pattern = re.compile(r'\[(\d+):(\d+\.?\d*)\](.*)')
        for line in text.splitlines():
            match = pattern.match(line)
            if match:
                m, s, content = match.groups()
                time_ms = (int(m) * 60 + float(s)) * 1000
                if content.strip():
                    self.lyric_data.append((time_ms, content.strip()))
                    item = QListWidgetItem(content.strip())
                    item.setTextAlignment(Qt.AlignCenter)
                    self.lyric_list.addItem(item)

    def switch_track(self, direction):
        count = self.musicList.rowCount()
        if count == 0: return
        next_row = (self.musicList.currentRow() + direction) % count
        self.musicList.setCurrentCell(next_row, 0)
        self.load_and_play(next_row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    player = MyMusicPlayer()
    player.show()
    sys.exit(app.exec())