# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'player.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSlider, QStackedWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1115, 634)
        Form.setMinimumSize(QSize(0, 50))
        Form.setStyleSheet(u"/* \u7ed9\u4e3b\u80cc\u666f\u8bbe\u7f6e\u5706\u89d2\u548c\u6df1\u8272\u4e3b\u9898 */\n"
"QWidget#MusicPlayer {\n"
"    background-color: #1e1e1e;\n"
"    color: #ffffff;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"/* \u7f8e\u5316\u8fdb\u5ea6\u6761 */\n"
"QSlider::groove:horizontal {\n"
"    height: 4px;\n"
"    background: #333;\n"
"    border-radius: 2px;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background: #0078d4;\n"
"    width: 12px;\n"
"    margin: -4px 0;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"/* \u5217\u8868\u6837\u5f0f */\n"
"QTableWidget {\n"
"    background-color: transparent;\n"
"    alternate-background-color: #252525;\n"
"    gridline-color: transparent;\n"
"    border: none;\n"
"}\n"
"QPushButton {\n"
"    border-radius: 5px;\n"
"    border: 1px solid #444;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #0078d4; /* \u84dd\u8272\u60ac\u505c\u611f */\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.setList = QListWidget(Form)
        self.setList.setObjectName(u"setList")
        self.setList.setMinimumSize(QSize(0, 0))
        self.setList.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_2.addWidget(self.setList)

        self.mainStacked = QStackedWidget(Form)
        self.mainStacked.setObjectName(u"mainStacked")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.mainStacked.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.mainStacked.addWidget(self.page_2)

        self.horizontalLayout_2.addWidget(self.mainStacked)

        self.musicList = QTableWidget(Form)
        self.musicList.setObjectName(u"musicList")
        self.musicList.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_2.addWidget(self.musicList)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.progressSlider = QSlider(Form)
        self.progressSlider.setObjectName(u"progressSlider")
        self.progressSlider.setMinimumSize(QSize(0, 0))
        self.progressSlider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout.addWidget(self.progressSlider)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 70))
        self.frame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.layoutWidget = QWidget(self.frame)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(160, 10, 782, 52))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.formerBtn = QPushButton(self.layoutWidget)
        self.formerBtn.setObjectName(u"formerBtn")
        self.formerBtn.setMinimumSize(QSize(100, 50))

        self.horizontalLayout.addWidget(self.formerBtn)

        self.playBtn = QPushButton(self.layoutWidget)
        self.playBtn.setObjectName(u"playBtn")
        self.playBtn.setMinimumSize(QSize(150, 50))

        self.horizontalLayout.addWidget(self.playBtn)

        self.nextBtn = QPushButton(self.layoutWidget)
        self.nextBtn.setObjectName(u"nextBtn")
        self.nextBtn.setMinimumSize(QSize(100, 50))

        self.horizontalLayout.addWidget(self.nextBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pauseBtn = QPushButton(self.layoutWidget)
        self.pauseBtn.setObjectName(u"pauseBtn")
        self.pauseBtn.setMinimumSize(QSize(100, 50))

        self.horizontalLayout.addWidget(self.pauseBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.listBtn = QPushButton(self.layoutWidget)
        self.listBtn.setObjectName(u"listBtn")
        self.listBtn.setMinimumSize(QSize(100, 50))

        self.horizontalLayout.addWidget(self.listBtn)

        self.radioSlider = QSlider(self.layoutWidget)
        self.radioSlider.setObjectName(u"radioSlider")
        self.radioSlider.setMinimumSize(QSize(200, 50))
        self.radioSlider.setMaximumSize(QSize(200, 100))
        self.radioSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.radioSlider)


        self.verticalLayout.addWidget(self.frame)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        self.mainStacked.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"MusicPlayer", None))
        self.formerBtn.setText(QCoreApplication.translate("Form", u"Previous", None))
        self.playBtn.setText(QCoreApplication.translate("Form", u"Play", None))
        self.nextBtn.setText(QCoreApplication.translate("Form", u"Next", None))
        self.pauseBtn.setText(QCoreApplication.translate("Form", u"Pause", None))
        self.listBtn.setText(QCoreApplication.translate("Form", u"MusicList", None))
    # retranslateUi

