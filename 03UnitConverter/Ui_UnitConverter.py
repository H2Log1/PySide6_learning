# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UnitConverter.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(396, 267)
        Form.setStyleSheet(u".QComboBox\n"
"{\n"
"	border-radius:5%;\n"
"	border:1px solid black;\n"
"}\n"
"\n"
".QLineEdit\n"
"{\n"
"	border-radius:5%;\n"
"	border:1px solid black;\n"
"}\n"
"\n"
".QPushButton\n"
"{\n"
"	border-radius:5%;\n"
"	border:1px solid black;\n"
"}\n"
"\n"
".QComboBox:hover{\n"
"	background-color: rgb(170, 255, 255);\n"
"}\n"
"\n"
".QLineEdit:hover{\n"
"	background-color: rgb(170, 255, 255);\n"
"}\n"
"\n"
".QPushButton:hover{\n"
"	background-color: rgb(170, 255, 255);\n"
"}\n"
"")
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.oneInputComboBox = QComboBox(Form)
        self.oneInputComboBox.setObjectName(u"oneInputComboBox")
        self.oneInputComboBox.setMinimumSize(QSize(192, 40))

        self.gridLayout_2.addWidget(self.oneInputComboBox, 3, 1, 1, 1)

        self.oneInputLineEdit = QLineEdit(Form)
        self.oneInputLineEdit.setObjectName(u"oneInputLineEdit")
        self.oneInputLineEdit.setMinimumSize(QSize(0, 40))

        self.gridLayout_2.addWidget(self.oneInputLineEdit, 3, 0, 1, 1)

        self.twoInputComboBox = QComboBox(Form)
        self.twoInputComboBox.setObjectName(u"twoInputComboBox")
        self.twoInputComboBox.setMinimumSize(QSize(0, 40))

        self.gridLayout_2.addWidget(self.twoInputComboBox, 4, 1, 1, 1)

        self.originDataLabel = QLabel(Form)
        self.originDataLabel.setObjectName(u"originDataLabel")
        self.originDataLabel.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(16)
        self.originDataLabel.setFont(font)

        self.gridLayout_2.addWidget(self.originDataLabel, 0, 0, 1, 1)

        self.dataTypeComboBox = QComboBox(Form)
        self.dataTypeComboBox.setObjectName(u"dataTypeComboBox")
        self.dataTypeComboBox.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.dataTypeComboBox, 2, 0, 1, 2)

        self.transDataLabel = QLabel(Form)
        self.transDataLabel.setObjectName(u"transDataLabel")
        self.transDataLabel.setMaximumSize(QSize(16777215, 50))
        font1 = QFont()
        font1.setPointSize(30)
        font1.setBold(True)
        self.transDataLabel.setFont(font1)

        self.gridLayout_2.addWidget(self.transDataLabel, 1, 0, 1, 1)

        self.twoInputLineEdit = QLineEdit(Form)
        self.twoInputLineEdit.setObjectName(u"twoInputLineEdit")
        self.twoInputLineEdit.setMinimumSize(QSize(0, 40))

        self.gridLayout_2.addWidget(self.twoInputLineEdit, 4, 0, 1, 1)

        self.calcBtn = QPushButton(Form)
        self.calcBtn.setObjectName(u"calcBtn")
        self.calcBtn.setMinimumSize(QSize(0, 30))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        self.calcBtn.setFont(font2)
        self.calcBtn.setIconSize(QSize(16, 16))
        self.calcBtn.setCheckable(False)
        self.calcBtn.setAutoRepeat(False)
        self.calcBtn.setAutoExclusive(False)

        self.gridLayout_2.addWidget(self.calcBtn, 6, 0, 1, 2)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"UnitConverter", None))
        self.oneInputLineEdit.setInputMask("")
        self.oneInputLineEdit.setText("")
        self.originDataLabel.setText(QCoreApplication.translate("Form", u"0=", None))
        self.transDataLabel.setText(QCoreApplication.translate("Form", u"0", None))
        self.twoInputLineEdit.setInputMask("")
        self.twoInputLineEdit.setText("")
        self.calcBtn.setText(QCoreApplication.translate("Form", u"\u8ba1\u7b97", None))
    # retranslateUi

