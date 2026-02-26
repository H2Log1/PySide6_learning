from PySide6.QtWidgets import QApplication, QWidget
from Ui_UnitConverter import Ui_Form

class MyWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)

        self.lengthVar = {'千米': 1000, '米': 1, '分米': 0.1, '厘米': 0.01}
        self.weightVar = {'千克': 1, '克': 0.001, '斤': 0.5}

        self.TypeDict = {
            '长度': self.lengthVar,
            '质量': self.weightVar
        }

        self.dataTypeComboBox.addItems(self.TypeDict.keys())
        self.oneInputComboBox.addItems(self.lengthVar.keys())
        self.twoInputComboBox.addItems(self.lengthVar.keys())

        self.bind()

    def bind(self):
        self.dataTypeComboBox.currentTextChanged.connect(self.typeChanged)
        self.calcBtn.clicked.connect(self.calc)

    def calc(self):
        try:
            value = float(self.oneInputLineEdit.text())
            dataType = self.dataTypeComboBox.currentText()            
            currentUnit = self.oneInputComboBox.currentText()
            transUnit = self.twoInputComboBox.currentText()

            standardValue = value * self.TypeDict[dataType][currentUnit]
            result = standardValue / self.TypeDict[dataType][transUnit]

            self.twoInputLineEdit.setText(str(result))
            self.originDataLabel.setText(f"{value} {currentUnit} = ")
            self.transDataLabel.setText(f"{result} {transUnit}")
        except ValueError:
            self.twoInputLineEdit.setText("输入错误！")

    def typeChanged(self, text):
        self.oneInputComboBox.clear()
        self.twoInputComboBox.clear()
        self.oneInputComboBox.addItems(self.TypeDict[text].keys())
        self.twoInputComboBox.addItems(self.TypeDict[text].keys())

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()