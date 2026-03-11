# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playerLite.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QSlider, QTableView,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(359, 138)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.musicTable = QTableView(Form)
        self.musicTable.setObjectName(u"musicTable")
        self.musicTable.setMinimumSize(QSize(300, 0))

        self.verticalLayout_2.addWidget(self.musicTable)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.progressSlider = QSlider(Form)
        self.progressSlider.setObjectName(u"progressSlider")
        self.progressSlider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout.addWidget(self.progressSlider)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.preBtn = QPushButton(Form)
        self.preBtn.setObjectName(u"preBtn")

        self.horizontalLayout.addWidget(self.preBtn)

        self.playBtn = QPushButton(Form)
        self.playBtn.setObjectName(u"playBtn")

        self.horizontalLayout.addWidget(self.playBtn)

        self.nextBtn = QPushButton(Form)
        self.nextBtn.setObjectName(u"nextBtn")

        self.horizontalLayout.addWidget(self.nextBtn)

        self.listBtn = QPushButton(Form)
        self.listBtn.setObjectName(u"listBtn")
        self.listBtn.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.listBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.volumeSlider = QSlider(Form)
        self.volumeSlider.setObjectName(u"volumeSlider")
        self.volumeSlider.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout_2.addWidget(self.volumeSlider)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"MusicPlayerLite", None))
        self.preBtn.setText(QCoreApplication.translate("Form", u"\u4e0a\u4e00\u9996", None))
        self.playBtn.setText(QCoreApplication.translate("Form", u"\u64ad\u653e", None))
        self.nextBtn.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u9996", None))
        self.listBtn.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165", None))
    # retranslateUi

