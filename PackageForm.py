import subprocess
from PyQt5 import uic
from Utils import *
from Frida_Project import default_UI_path
import Information

class PackageForm(QDialog):
    def __init__(self, parent=None):
        super(PackageForm, self).__init__(parent)
        self.ui = uic.loadUi(default_UI_path + "package.ui", self)

        self.clickRefresh()
        self.ui.lstPackage.setColumnWidth(1, 110)
        self.show()

    def clickRefresh(self):
        result = subprocess.check_output("frida-ps -Uai")
        self.ui.lstPackage.setRowCount(len(result.decode('utf-8').split('\r\n')) - 3)
        for x, str in enumerate(result.decode('utf-8').split('\r\n')):
            if x < 2:
                continue
            x -= 2

            splitData = str.split()
            if len(splitData) < 3:
                continue

            for y, str2 in enumerate(splitData):
                if y == 0 or y == 1 or y == len(splitData) - 1:
                    if y == 1 and len(splitData) > 3:
                        str2 = ' '.join(splitData[1:len(splitData) - 1])

                    if y == len(splitData) - 1:
                        y = 2

                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setText(str2)
                    self.ui.lstPackage.setItem(x, y, item)

    def clickOk(self):
        try:
            info.package_name = self.ui.lstPackage.item(self.ui.lstPackage.currentRow(), 2).text()
            info.process_name = self.ui.lstPackage.item(self.ui.lstPackage.currentRow(), 1).text()
            
        except Exception as e:
            return
        self.close()