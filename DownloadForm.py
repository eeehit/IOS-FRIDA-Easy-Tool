from PyQt5 import uic
from Utils import *
from Frida_Project import default_UI_path, default_File_path
import requests, json, os
import Information

class DownloadForm(QDialog):
    def __init__(self, parent=None):
        super(DownloadForm, self).__init__(parent)
        self.ui = uic.loadUi(default_UI_path + "download.ui", self)

        self.getRepositoryList()
        self.show()

    def getRepositoryList(self):
        try:
            URL = info.ipAddress + '/getRepositoryList'
            response = requests.get(URL)
            response_json = json.loads(response.text)

            self.ui.lstRepo.setRowCount(len(response_json['data']))
            for i, repo, in enumerate(response_json['data']):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setText(repo)
                self.ui.lstRepo.setItem(i, 0, item)
        except Exception as e:
            print('[!] getRepositoryList() Error : ' + str(e))

    def clickDownload(self):
        try:
            selectedItems = self.ui.lstRepo.selectedItems()
            if len(selectedItems) > 0:
                repo_title = selectedItems[0].text()

                URL = info.ipAddress + '/getRepository'
                params = {'repo_title': repo_title}
                response = requests.get(URL, params=params)
                response_json = json.loads(response.text)

                if response_json['data'] == -1:
                    QMessageBox.warning(self, 'Warning', 'UnCorrect Repository!!!')
                    return
                else:
                    selectItem = info.mainUI.ui.treeScriptList.currentItem()
                    dirPath = selectPath(selectItem, repo_title)

                    if not (os.path.isdir(dirPath)):
                        os.makedirs(os.path.join(dirPath))
                    else:
                        pass

                    for files in response_json['data']:
                        path = os.path.join(dirPath + "\\" + files['title'])
                        print("create " + path)
                        fid = open(path, "w")
                        fid.write(files['content'])
                        fid.close()
                info.mainUI.ui.treeScriptList.clear()
                createFileSystem(default_File_path + 'User_script\\', info.mainUI.ui.treeScriptList)
                self.close()
        except Exception as e:
            print('[!] clickDownload() Error : ' + str(e))