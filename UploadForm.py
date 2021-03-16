from PyQt5 import uic
from Utils import *
from Frida_Project import default_UI_path
import requests, json, os
import Information

class UploadForm(QDialog):
    def __init__(self, parent=None):
        super(UploadForm, self).__init__(parent)
        self.ui = uic.loadUi(default_UI_path + "upload.ui", self)

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

    def clickCreateRepo(self):
        pass

    def clickUpload(self):
        try:
            selectedItems = self.ui.lstRepo.selectedItems()
            if len(selectedItems) > 0:
                repo_title = selectedItems[0].text()
                URL0 = info.ipAddress + '/getRepositoryId'
                params = {'repo_title':repo_title}
                response = requests.get(URL0, params=params)
                response_json = json.loads(response.text)

                repo_id = response_json['data']
                if repo_id != -1:
                    treeSelectedItems = info.mainUI.treeScriptList.selectedItems()
                    if len(treeSelectedItems) > 0:
                        URL1 = info.ipAddress + '/postCheckName'
                        URL2 = info.ipAddress + '/createPost'

                        allFile = []
                        for treeSelectedItem in treeSelectedItems:
                            path = getAbsPath(treeSelectedItem, 0)

                            if os.path.exists(path):
                                allFile.extend(getAllFile(path))

                        for file in allFile:
                            params = {'repo_id':repo_id, 'title':file.split('\\')[-1]}
                            response = requests.get(URL1, params=params)
                            response_json = json.loads(response.text)

                            if len(response_json['data']) > 0:
                                reply = QMessageBox.information(self, 'Question',
                                                                'File: ' + file.split('\\')[-1] + '\nFile already exists. Do you want to overwrite it?',
                                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                if reply == QMessageBox.No:
                                    return
                            f = open(file, 'r')
                            params = {'repo_id':repo_id, 'title':file.split('\\')[-1], 'content':f.read()}
                            requests.get(URL2, params=params)
                            f.close()
                        self.close()
                    else:
                        QMessageBox.warning(self, 'Warning', 'Please select a file to upload first.')
                        return

        except Exception as e:
            print('[!] clickUpload() Error : ' + str(e))