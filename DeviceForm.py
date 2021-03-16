from PyQt5 import uic, QtCore
from Utils import *
from Frida_Project import default_UI_path
import Information

class DeviceForm(QDialog):
    def __init__(self, parent=None):
        super(DeviceForm, self).__init__(parent)
        self.ui = uic.loadUi(default_UI_path + "device.ui", self)

        self.clickRefresh()
        self.show()

    def clickRefresh(self):
        self.ui.lstDevice.clear()
        getDevices()
        for i in info.device_dict.values():
            self.ui.lstDevice.addItem(str(i))

    def clickOk(self):
        try:
            setDevice(self.ui.lstDevice.currentItem().text()[11:51])
            info.mainUI.ui.deviceLabel.setText(': ' + self.ui.lstDevice.currentItem().text()[11:51])
            info.mainUI.ui.repaint()
        except Exception as e:
            return
        self.close()