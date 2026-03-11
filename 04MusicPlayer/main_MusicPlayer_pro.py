import sys
import os
import re
import json
import base64
import requests
from PySide6.QtWidgets import (QApplication, QWidget, QTableWidgetItem, 
                             QHeaderView, QFileDialog, QLabel, QVBoxLayout, 
                             QListWidget, QListWidgetItem)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Qt, QPoint, QThread, Signal
from PySide6.QtGui import QPixmap, QImage, QMouseEvent

# 导入你的 UI 类
from Ui_player import Ui_Form

_SESSION = requests.Session()
_SESSION.headers.update({"User-Agent": "MusicPlayer/1.0"})


# ============ QQ 音乐 API ============
def qq_music_search(keyword, limit=5):
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    payload = {
        "comm": {"ct": 11, "cv": "12080008"},
        "request": {
            "module": "music.search.SearchCgiService",
            "method": "DoSearchForQQMusicDesktop",
            "param": {"query": keyword, "num_per_page": limit, "page_num": 1, "search_type": 0}
        }
    }
    resp = _SESSION.post(url, json=payload, headers={"Referer": "https://y.qq.com"}, timeout=8)
    return resp.json().get("request", {}).get("data", {}).get("body", {}).get("song", {}).get("list", [])

def qq_music_lyric(song_mid):
    url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
    resp = _SESSION.get(url, params={"songmid": song_mid, "format": "json", "nobase64": 0},
                        headers={"Referer": "https://y.qq.com"}, timeout=8)
    b64 = resp.json().get("lyric", "")
    return base64.b64decode(b64).decode("utf-8", errors="ignore") if b64 else ""

def qq_music_cover(album_mid, size=300):
    url = f"https://y.gtimg.cn/music/photo_new/T002R{size}x{size}M000{album_mid}.jpg"
    resp = _SESSION.get(url, timeout=8)
    return resp.content if resp.status_code == 200 and len(resp.content) > 1000 else None


# ============ 网易云音乐 API ============
def netease_search(keyword, limit=5):
    url = "https://music.163.com/api/search/get/web"
    data = {"s": keyword, "type": 1, "limit": limit, "offset": 0}
    headers = {"Referer": "https://music.163.com"}
    resp = _SESSION.post(url, data=data, headers=headers, timeout=8)
    return resp.json().get("result", {}).get("songs", [])

def netease_lyric(song_id):
    url = f"https://music.163.com/api/song/lyric"
    resp = _SESSION.get(url, params={"id": song_id, "lv": 1, "tv": -1},
                        headers={"Referer": "https://music.163.com"}, timeout=8)
    return resp.json().get("lrc", {}).get("lyric", "")

def netease_cover(album_id, size=300):
    """通过专辑详情接口获取封面 URL 再下载"""
    url = f"https://music.163.com/api/album/{album_id}"
    resp = _SESSION.get(url, headers={"Referer": "https://music.163.com"}, timeout=8)
    pic_url = resp.json().get("album", {}).get("picUrl", "")
    if pic_url:
        img = _SESSION.get(f"{pic_url}?param={size}y{size}", timeout=8)
        if img.status_code == 200 and len(img.content) > 1000:
            return img.content
    return None


# ============ Deezer API ============
def deezer_search(keyword, limit=3):
    resp = _SESSION.get("https://api.deezer.com/search",
                        params={"q": keyword, "limit": limit}, timeout=8)
    return resp.json().get("data", [])

def deezer_cover(album_id):
    """Deezer 封面直接从 album cover URL 获取"""
    resp = _SESSION.get(f"https://api.deezer.com/album/{album_id}", timeout=8)
    cover_url = resp.json().get("cover_xl") or resp.json().get("cover_big", "")
    if cover_url:
        img = _SESSION.get(cover_url, timeout=8)
        return img.content if img.status_code == 200 else None
    return None


# --- 后台抓取线程 ---
class FetcherWorker(QThread):
    """后台线程：负责在线搜索歌词和封面"""
    finished = Signal(dict)

    def __init__(self, title, artist, duration_ms):
        super().__init__()
        self.title = title
        self.artist = artist
        self.duration_ms = duration_ms

    def run(self):
        result = {"lyrics": None, "cover_data": None}
        
        first_artist = self.artist.split(',')[0].strip()
        search_terms = [
            (first_artist, self.title),
            ("", self.title),
        ]

        # ==================== 1. 歌词搜索 ====================
        
        # 1a. LRCLIB 精确匹配
        try:
            params = {'artist_name': first_artist, 'track_name': self.title, 'duration': self.duration_ms // 1000}
            print(f"[LRCLIB/get] 请求: {params}")
            resp = _SESSION.get("https://lrclib.net/api/get", params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                result["lyrics"] = data.get('syncedLyrics') or data.get('plainLyrics')
                if result["lyrics"]: print("[LRCLIB/get] 命中")
        except Exception as e:
            print(f"[LRCLIB/get] 失败: {e}")

        # 1b. LRCLIB 模糊搜索
        if not result["lyrics"]:
            for artist, title in search_terms:
                try:
                    q = f"{artist} {title}".strip()
                    resp = _SESSION.get("https://lrclib.net/api/search", params={'q': q}, timeout=5)
                    if resp.status_code == 200 and resp.json():
                        item = resp.json()[0]
                        result["lyrics"] = item.get('syncedLyrics') or item.get('plainLyrics')
                        if result["lyrics"]:
                            print(f"[LRCLIB/search] 命中: {item.get('trackName')}")
                            break
                except Exception as e:
                    print(f"[LRCLIB/search] 失败: {e}")

        # 1c. 网易云音乐歌词
        if not result["lyrics"]:
            for artist, title in search_terms:
                try:
                    keyword = f"{artist} {title}".strip()
                    print(f"[网易云/歌词] 搜索: {keyword}")
                    songs = netease_search(keyword, limit=3)
                    for song in songs:
                        lrc = netease_lyric(song["id"])
                        if lrc and '[' in lrc:
                            result["lyrics"] = lrc
                            artists = '/'.join(a['name'] for a in song.get('artists', []))
                            print(f"[网易云/歌词] 命中: {song['name']} - {artists}")
                            break
                    if result["lyrics"]: break
                except Exception as e:
                    print(f"[网易云/歌词] 失败: {e}")

        # 1d. QQ音乐歌词
        if not result["lyrics"]:
            for artist, title in search_terms:
                try:
                    keyword = f"{artist} {title}".strip()
                    print(f"[QQ音乐/歌词] 搜索: {keyword}")
                    songs = qq_music_search(keyword, limit=3)
                    for song in songs:
                        mid = song.get("mid", "")
                        if mid:
                            lrc = qq_music_lyric(mid)
                            if lrc and '[' in lrc:
                                result["lyrics"] = lrc
                                singer = song.get('singer', [{}])[0].get('name', '?')
                                print(f"[QQ音乐/歌词] 命中: {song.get('name')} - {singer}")
                                break
                    if result["lyrics"]: break
                except Exception as e:
                    print(f"[QQ音乐/歌词] 失败: {e}")

        # ==================== 2. 封面搜索 ====================

        # 2a. 网易云音乐封面
        for artist, title in search_terms:
            if result["cover_data"]: break
            try:
                keyword = f"{artist} {title}".strip()
                print(f"[网易云/封面] 搜索: {keyword}")
                songs = netease_search(keyword, limit=1)
                if songs:
                    album_id = songs[0].get("album", {}).get("id")
                    if album_id:
                        cover = netease_cover(album_id)
                        if cover:
                            result["cover_data"] = cover
                            print(f"[网易云/封面] 命中: {songs[0]['name']}")
            except Exception as e:
                print(f"[网易云/封面] 失败: {e}")

        # 2b. QQ音乐封面
        if not result["cover_data"]:
            for artist, title in search_terms:
                if result["cover_data"]: break
                try:
                    keyword = f"{artist} {title}".strip()
                    print(f"[QQ音乐/封面] 搜索: {keyword}")
                    songs = qq_music_search(keyword, limit=1)
                    if songs:
                        album_mid = songs[0].get("album", {}).get("mid", "")
                        if album_mid:
                            cover = qq_music_cover(album_mid)
                            if cover:
                                result["cover_data"] = cover
                                print(f"[QQ音乐/封面] 命中: {songs[0].get('name')}")
                except Exception as e:
                    print(f"[QQ音乐/封面] 失败: {e}")

        # 2c. Deezer 封面
        if not result["cover_data"]:
            for artist, title in search_terms:
                if result["cover_data"]: break
                try:
                    keyword = f"{artist} {title}".strip()
                    print(f"[Deezer/封面] 搜索: {keyword}")
                    tracks = deezer_search(keyword, limit=1)
                    if tracks:
                        album_id = tracks[0].get("album", {}).get("id")
                        if album_id:
                            cover = deezer_cover(album_id)
                            if cover:
                                result["cover_data"] = cover
                                print(f"[Deezer/封面] 命中: {tracks[0].get('title')}")
                except Exception as e:
                    print(f"[Deezer/封面] 失败: {e}")

        # 2d. iTunes 封面（兜底）
        if not result["cover_data"]:
            for artist, title in search_terms:
                if result["cover_data"]: break
                try:
                    term = f"{artist} {title}".strip()
                    resp = _SESSION.get("https://itunes.apple.com/search",
                                        params={'term': term, 'entity': 'song', 'limit': 1}, timeout=5)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data['resultCount'] > 0:
                            img_url = data['results'][0]['artworkUrl100'].replace('100x100', '600x600')
                            result["cover_data"] = _SESSION.get(img_url, timeout=5).content
                            print("[iTunes/封面] 命中")
                except Exception as e:
                    print(f"[iTunes] 失败: {e}")

        self.finished.emit(result)

# --- 主窗口类 ---
class MyMusicPlayer(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #
        

        self.setFixedSize(self.width(), self.height())

        # --- 音频引擎 ---
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        self.lyric_data = [] 
        self.init_ui_logic()
        self.init_connections()

    # --- 窗口拖动逻辑 ---
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            new_pos = event.globalPosition().toPoint()
            self.move(self.pos() + (new_pos - self._drag_pos))
            self._drag_pos = new_pos

    def init_ui_logic(self):
        """初始化 UI 状态"""
        self.setList.addItems(["音乐封面", "同步歌词"])
        self.setList.currentRowChanged.connect(self.handle_view_switch)
        
        # 封面显示
        self.cover_layout = QVBoxLayout(self.page)
        self.cover_label = QLabel("等待播放...")
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_layout.addWidget(self.cover_label)

        # 歌词显示
        self.lyric_layout = QVBoxLayout(self.page_2)
        self.lyric_list = QListWidget()
        self.lyric_list.setStyleSheet("""
            QListWidget { background: transparent; border: none; color: #888; font-size: 16px; outline: none; }
            QListWidget::item { padding: 10px; border: none; }
            QListWidget::item:selected { color: #00d4ff; font-size: 20px; font-weight: bold; background: transparent; }
        """)
        self.lyric_layout.addWidget(self.lyric_list)

        # 列表配置
        self.musicList.setColumnCount(3)
        self.musicList.setHorizontalHeaderLabels(["歌名", "格式", "路径"])
        self.musicList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.musicList.setColumnHidden(2, True)

        self.radioSlider.setRange(0, 100)
        self.radioSlider.setValue(50)

    def handle_view_switch(self, index):
        """沉浸模式：切换到歌词页时隐藏右侧栏"""
        self.mainStacked.setCurrentIndex(index)
        self.musicList.setVisible(index == 0)

    def init_connections(self):
        """信号绑定"""
        self.listBtn.clicked.connect(self.import_music)
        self.playBtn.clicked.connect(self.handle_play_press)
        self.pauseBtn.clicked.connect(self.player.pause)
        self.nextBtn.clicked.connect(lambda: self.switch_track(1))
        self.formerBtn.clicked.connect(lambda: self.switch_track(-1))
        
        self.musicList.itemDoubleClicked.connect(self.play_selected_row)
        
        self.radioSlider.valueChanged.connect(lambda v: self.audio_output.setVolume(v / 100))
        
        # 进度条修复逻辑
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.positionChanged.connect(self.sync_ui_with_postition)
        self.progressSlider.sliderMoved.connect(self.player.setPosition)

    # --- 核心播放逻辑 ---

    def on_duration_changed(self, duration):
        """当媒体时长就绪时，更新进度条并启动在线抓取"""
        self.progressSlider.setRange(0, duration)
        if duration > 0 and hasattr(self, '_pending_path'):
            self.start_online_fetch(self._pending_path, duration)
            del self._pending_path

    def import_music(self):
        files, _ = QFileDialog.getOpenFileNames(self, "导入音乐", "", "音频 (*.mp3 *.flac *.wav)")
        if files:
            for f in files:
                row = self.musicList.rowCount()
                self.musicList.insertRow(row)
                self.musicList.setItem(row, 0, QTableWidgetItem(os.path.basename(f)))
                self.musicList.setItem(row, 1, QTableWidgetItem(os.path.splitext(f)[1].upper()))
                self.musicList.setItem(row, 2, QTableWidgetItem(f))

    def play_selected_row(self, item):
        self.load_and_play(item.row())

    def handle_play_press(self):
        if self.player.playbackState() == QMediaPlayer.PausedState:
            self.player.play()
        else:
            curr = self.musicList.currentRow()
            if curr != -1: self.load_and_play(curr)

    def load_and_play(self, row):
        file_path = self.musicList.item(row, 2).text()
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self._pending_path = file_path  # 记录路径，等 duration 就绪后再抓取
        self.update_metadata_source(file_path) # 解析本地元数据
        self.player.play()
        self.musicList.selectRow(row)

    @staticmethod
    def parse_filename(path):
        """从文件名智能解析 artist 和 title（无标签时的回退方案）"""
        name = os.path.splitext(os.path.basename(path))[0]  # 去掉扩展名
        # 清理下划线为空格
        name = name.replace('_', ' ')
        # 常见分隔符: " - ", " – ", "－"
        for sep in [' - ', ' – ', '－']:
            if sep in name:
                parts = name.split(sep, 1)
                return parts[0].strip(), parts[1].strip()
        # 如果有逗号分隔的多个艺术家前缀，尝试取最后一段
        # 例如 "鸣潮先约电台, jixwang, 小林未郁 - 那颗星梦见的春日"
        return "Unknown", name.strip()

    def update_metadata_source(self, path):
        """优先读取本地元数据（封面、歌词）"""
        from mutagen import File
        try:
            audio = File(path)
            if audio is None:
                return
            
            # 先从文件名解析作为默认值
            fallback_artist, fallback_title = self.parse_filename(path)
            title = fallback_title
            artist = fallback_artist

            # 尝试从标签读取基础信息（标签优先级更高）
            if audio.tags:
                tag_artist = audio.tags.get('TPE1')
                tag_title = audio.tags.get('TIT2')
                if tag_artist: artist = str(tag_artist[0])
                if tag_title: title = str(tag_title[0])

            self._meta_title = title
            self._meta_artist = artist

            # 1. 本地封面
            cover_data = None
            if audio.tags:
                if 'APIC:' in audio.tags: cover_data = audio.tags['APIC:'].data
                elif hasattr(audio, 'pictures') and audio.pictures: cover_data = audio.pictures[0].data

            # 2. 本地歌词
            lyric_text = ""
            if audio.tags:
                uslt = [v for k, v in audio.tags.items() if k.startswith('USLT')]
                if uslt: lyric_text = uslt[0].text

            self._has_local_cover = cover_data is not None
            self._has_local_lyrics = bool(lyric_text)

            # 应用已有的本地数据
            if cover_data:
                self.apply_cover(cover_data)
            else:
                self.cover_label.setText("正在联网搜索封面...")

            if lyric_text:
                self.parse_lyrics(lyric_text)
            else:
                self.lyric_list.clear()
                self.lyric_list.addItem("正在联网搜索歌词...")

        except Exception as e:
            print(f"[元数据读取失败] {e}")
            self._meta_title = os.path.basename(path)
            self._meta_artist = "Unknown"
            self._has_local_cover = False
            self._has_local_lyrics = False

    def start_online_fetch(self, path, duration_ms):
        """当本地缺封面或歌词时，启动后台联网抓取（duration 已就绪）"""
        if getattr(self, '_has_local_cover', True) and getattr(self, '_has_local_lyrics', True):
            return  # 本地数据完整，无需联网
        title = getattr(self, '_meta_title', os.path.basename(path))
        artist = getattr(self, '_meta_artist', 'Unknown')
        print(f"[联网抓取] title={title}, artist={artist}, duration={duration_ms}ms")
        self.fetcher = FetcherWorker(title, artist, duration_ms)
        self.fetcher.finished.connect(self.apply_online_metadata)
        self.fetcher.start()

    def apply_online_metadata(self, data):
        """将网络抓取结果应用到 UI"""
        if data["cover_data"]: self.apply_cover(data["cover_data"])
        if data["lyrics"]: self.parse_lyrics(data["lyrics"])
        else: 
            if self.lyric_list.count() > 0 and "正在联网" in self.lyric_list.item(0).text():
                self.lyric_list.clear(); self.lyric_list.addItem("未找到歌词")

    def apply_cover(self, data):
        img = QImage.fromData(data)
        pix = QPixmap.fromImage(img).scaled(380, 380, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cover_label.setPixmap(pix)

    def parse_lyrics(self, text):
        self.lyric_data = []
        self.lyric_list.clear()
        pattern = re.compile(r'\[(\d+):(\d+\.?\d*)\](.*)')
        for line in text.splitlines():
            match = pattern.match(line)
            if match:
                m, s, content = match.groups()
                time_ms = (int(m) * 60 + float(s)) * 1000
                if content.strip():
                    self.lyric_data.append((time_ms, content.strip()))
                    item = QListWidgetItem(content.strip()); item.setTextAlignment(Qt.AlignCenter)
                    self.lyric_list.addItem(item)

    def sync_ui_with_postition(self, pos):
        """同步进度条与歌词滚动"""
        if not self.progressSlider.isSliderDown():
            self.progressSlider.setValue(pos)
        
        if self.lyric_data:
            idx = 0
            for i, (t, txt) in enumerate(self.lyric_data):
                if pos >= t: idx = i
                else: break
            self.lyric_list.setCurrentRow(idx)
            self.lyric_list.scrollToItem(self.lyric_list.currentItem(), QListWidget.PositionAtCenter)

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