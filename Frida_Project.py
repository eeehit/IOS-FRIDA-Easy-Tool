import sys, subprocess, os, re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
from PyQt5 import uic, QtCore
from Utils import *
import paramiko
from DeviceForm import *
from PackageForm import *
from UploadForm import *
from DownloadForm import *

form_class = uic.loadUiType(default_UI_path + "frida.ui")[0]

class Form(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(default_UI_path + "frida.ui", self)
        self.setupUi(self)

        self.interceptorButtonGroup = QButtonGroup()
        self.interceptorButtonGroup.buttonClicked[int].connect(self.clickInterceptor_ButtonGroup)
        self.implButtonGroup = QButtonGroup()
        self.implButtonGroup.buttonClicked[int].connect(self.clickImpl_ButtonGroup)

        self.txtPlayScript_Edit.keyPressEvent = self._txtPlayScript_Edit_keyPressEvent
        self.txtPlayScript_Edit.wheelEvent = self._txtPlayScript_Edit_wheelEvent
        self.txtScriptEdit.keyPressEvent = self._txtScriptEdit_keyPressEvent
        self.txtScriptEdit.wheelEvent = self._txtScriptEdit_wheelEvent
        self.txtImpl_Function.keyPressEvent = self._txtImpl_Function_keyPressEvent
        self.txtImpl_Function.wheelEvent = self._txtImpl_Function_wheelEvent
        self.txtClassScript.keyPressEvent = self._txtClassScript_keyPressEvent
        self.txtClassScript.wheelEvent = self._txtClassScript_wheelEvent
        self.txtMethodScript.keyPressEvent = self._txtMethodScript_keyPressEvent
        self.txtMethodScript.wheelEvent = self._txtMethodScript_wheelEvent
        self.show()

    ####### QPlanTextEdit Event Handler #######
    def _txtPlayScript_Edit_keyPressEvent(self, event):
        if (event.key() == Qt.Key_Tab):
            self.txtPlayScript_Edit.insertPlainText(" " * 4)
        else:
            QPlainTextEdit.keyPressEvent(self.txtPlayScript_Edit, event)
    def _txtPlayScript_Edit_wheelEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            self._txtPlayScript_Edit_zoom(event.angleDelta().y())
        else:
            QPlainTextEdit.wheelEvent(self.txtPlayScript_Edit, event)
    def _txtPlayScript_Edit_zoom(self, delta):
        if delta < 0:
            self.txtPlayScript_Edit.zoomOut(2)
        elif delta > 0:
            self.txtPlayScript_Edit.zoomIn(2)
    def _txtScriptEdit_keyPressEvent(self, event):
        if (event.key() == Qt.Key_Tab):
            self.txtScriptEdit.insertPlainText(" " * 4)
        else:
            QPlainTextEdit.keyPressEvent(self.txtScriptEdit, event)
    def _txtScriptEdit_wheelEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            self._txtScriptEdit_zoom(event.angleDelta().y())
        else:
            QPlainTextEdit.wheelEvent(self.txtScriptEdit, event)
    def _txtScriptEdit_zoom(self, delta):
        if delta < 0:
            self.txtScriptEdit.zoomOut(2)
        elif delta > 0:
            self.txtScriptEdit.zoomIn(2)
    def _txtImpl_Function_keyPressEvent(self, event):
        if (event.key() == Qt.Key_Tab):
            self.txtImpl_Function.insertPlainText(" " * 4)
        else:
            QPlainTextEdit.keyPressEvent(self.txtImpl_Function, event)
    def _txtImpl_Function_wheelEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            self._txtImpl_Function_zoom(event.angleDelta().y())
        else:
            QPlainTextEdit.wheelEvent(self.txtImpl_Function, event)
    def _txtImpl_Function_zoom(self, delta):
        if delta < 0:
            self.txtImpl_Function.zoomOut(2)
        elif delta > 0:
            self.txtImpl_Function.zoomIn(2)
    def _txtClassScript_keyPressEvent(self, event):
        if (event.key() == Qt.Key_Tab):
            self.txtClassScript.insertPlainText(" " * 4)
        else:
            QPlainTextEdit.keyPressEvent(self.txtClassScript, event)
    def _txtClassScript_wheelEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            self._txtClassScript_zoom(event.angleDelta().y())
        else:
            QPlainTextEdit.wheelEvent(self.txtClassScript, event)
    def _txtClassScript_zoom(self, delta):
        if delta < 0:
            self.txtClassScript.zoomOut(2)
        elif delta > 0:
            self.txtClassScript.zoomIn(2)
    def _txtMethodScript_keyPressEvent(self, event):
        if (event.key() == Qt.Key_Tab):
            self.txtMethodScript.insertPlainText(" " * 4)
        else:
            QPlainTextEdit.keyPressEvent(self.txtMethodScript, event)
    def _txtMethodScript_wheelEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            self._txtMethodScript_zoom(event.angleDelta().y())
        else:
            QPlainTextEdit.wheelEvent(self.txtMethodScript, event)
    def _txtMethodScript_zoom(self, delta):
        if delta < 0:
            self.txtMethodScript.zoomOut(2)
        elif delta > 0:
            self.txtMethodScript.zoomIn(2)

    def enumClass(self):
        try:
            self.ui.EnumStack.setCurrentIndex(2)
        except Exception as e:
            print('[!] enumClass() Error : ' + str(e))
    def enumMethod(self):
        try:
            self.ui.EnumStack.setCurrentIndex(0)
        except Exception as e:
            print('[!] enumMethod() Error : ' + str(e))
    def enumScript(self):
        try:
            self.ui.txtScriptEdit.setEnabled(False)
            self.ui.treeScriptList.clear()
            createFileSystem(default_File_path + 'User_script\\', self.ui.treeScriptList)
            self.ui.EnumStack.setCurrentIndex(1)
        except Exception as e:
            print('[!] enumScript() Error : ' + str(e))
    def clickDevice(self):
        try:
            deviceForm = DeviceForm(self)
            deviceForm.exec_()

            if info.device != None:
                self.ui.btnPackage.setEnabled(True)
                self.ui.btnDevice.setEnabled(False)
        except Exception as e:
            print('[!] clickDevice() Error : ' + str(e))
    def clickPackage(self):
        try:
            packageForm = PackageForm(self)
            packageForm.exec_()

            if info.package_name != '' and info.process_name != '':
                self.init()

                f = open(default_File_path + "searchClass.js", "r")
                data = f.read()
                data = data.replace('\t', '    ')
                self.ui.txtClassScript.setPlainText(data)
                f.close()
        except Exception as e:
            print('[!] clickPackage() Error : ' + str(e))

    def init(self):
        try:
            self.ui.packageLabel.setText(': ' + info.package_name)
            self.ui.repaint()
            self.ui.tabWidget.setEnabled(True)

            self.ui.lstMethodResult.setContextMenuPolicy(Qt.CustomContextMenu)
            self.ui.lstMethodResult.customContextMenuRequested.connect(self.__method_context_menu)

            self.ui.treeScriptList.setContextMenuPolicy(Qt.CustomContextMenu)
            self.ui.treeScriptList.customContextMenuRequested.connect(self.__list_context_menu)

            self.ui.lstMemoryScan_Result.setContextMenuPolicy(Qt.CustomContextMenu)
            self.ui.lstMemoryScan_Result.customContextMenuRequested.connect(self.__memory_context_menu)
            self.ui.lstMemoryScan_Result.setColumnWidth(0, 90)
            self.ui.lstMemoryScan_Address.setColumnWidth(0, 125)
            self.ui.txtMemoryDump_path.setText(default_Output_path + "Dump\\")

            self.ui.lstInterceptor_Current.setColumnWidth(0, 222)
            self.ui.lstInterceptor_Current.setColumnWidth(1, 222)

            self.ui.lstImpl_Current.setColumnWidth(0, 222)
            self.ui.lstImpl_Current.setColumnWidth(1, 222)
        except Exception as e:
            print('[!] init() Error : ' + str(e))

    def function_init(self):
        info.isMemPatch = False
        info.isPlay = False
        info.isImpl = False
        info.isIntercept = False
        info.isTrace = False
        info.isDebug = False
        self.ui.labelTrace_Status.setText('Stop')
        self.ui.labelTrace_Status.setStyleSheet('Color: Black')

    ##########################
    #   Enumerator - Class   #
    ##########################
    def clickClassLoad(self):
        try:
            self.function_init()
            info.script_to_load = self.ui.txtClassScript.toPlainText().replace('send(', 'send(\'clazzclazz\'+')
            loadScript()
        except Exception as e:
            print('[!] clickClassLoad() Error : ' + str(e))

    def clickClassClear(self):
        try:
            if len(info.classList) <= 0:
                return
            self.ui.lstClassResult.horizontalHeaderItem(0).setText('NAME (0)')
            info.classList.clear()
            self.ui.txtClassResearch.setText('')
            self.ui.lstClassResult.setRowCount(0)
        except Exception as e:
            print('[!] clickClassClear() Error : ' + str(e))

    def clickClassSave(self):
        try:
            if len(info.classList) <= 0:
                return
            saveScript(self.ui.txtMethodScript.toPlainText().replace('    ', '\t'), 0)
        except Exception as e:
            print('[!] clickClassSave() Error : ' + str(e))

    def clickClassExtract(self):
        try:
            if len(info.classList) <= 0:
                return
            extractContent('\n'.join(info.classList))
        except Exception as e:
            print('[!] clickClassExtract() Error : ' + str(e))

    def changeClassSearch(self, QString):
        try:
            self.ui.lstClassResult.clear()
            classList = [x for x in info.classList if QString.lower() in x.lower()]

            self.ui.lstClassResult.setRowCount(len(classList))
            info.mainUI.ui.lstClassResult.setHorizontalHeaderLabels([''.join(['Name (', str(len(classList)), ')'])])
            for i in range(len(classList)):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setText(classList[i])
                info.mainUI.ui.lstClassResult.setItem(0, i, item)

            info.mainUI.ui.update()
        except Exception as e:
            print('[!] changeClassSearch() Error : ' + str(e))

    def doubleClassSelect(self, QModelIndex):
        try:
            self.ui.EnumStack.setCurrentIndex(0)
            self.ui.txtMethodClassName.setText(self.ui.lstClassResult.item(QModelIndex.row(), QModelIndex.column()).text())
        except Exception as e:
            print('[!] doubleClassSelect() Error : ' + str(e))



    ###########################
    #   Enumerator - Method   #
    ###########################
    def clickMethodCreate(self):
        try:
            if self.ui.txtMethodClassName.text() not in info.classList:
                QMessageBox.warning(info.mainUI, 'Faild', 'This ClassName does not exist!\r\nPlease do classList load first.')
                return

            renderScript(default_File_path + "searchMethod.js", self.ui.txtMethodClassName.text())

            f = open(default_File_path + "searchMethod_tmp.js", "r")
            data = f.read()
            data = data.replace('\t', '    ')
            self.ui.txtMethodScript.setPlainText(data)
            f.close()
            os.remove(default_File_path + "searchMethod_tmp.js")
        except Exception as e:
            print('[!] clickMethodCreate() Error : ' + str(e))

    def clickMethodLoad(self):
        try:
            self.function_init()
            info.script_to_load = self.ui.txtMethodScript.toPlainText().replace('send(', 'send(\'mm33tthh00dd\'+')
            loadScript()
        except Exception as e:
            print('[!] clickMethodLoad() Error : ' + str(e))

    def clickMethodClear(self):
        try:
            if len(info.currentMethodList) <= 0:
                return
            self.ui.lstMethodResult.horizontalHeaderItem(0).setText('NAME (0)')
            info.currentMethodList.clear()
            self.ui.txtMethodResearch.setText('')
            self.ui.lstMethodResult.setRowCount(0)
        except Exception as e:
            print('[!] clickMethodClear() Error : ' + str(e))

    def clickMethodSave(self):
        try:
            if len(info.currentMethodList) <= 0:
                return
            saveScript(self.ui.txtClassScript.toPlainText().replace('    ', '\t'), 0)
        except Exception as e:
            print('[!] clickMethodSave() Error : ' + str(e))

    def clickMethodExtract(self):
        try:
            if len(info.currentMethodList) <= 0:
                return
            extractContent('\n'.join(info.currentMethodList))
        except Exception as e:
            print('[!] clickMethodExtract() Error : ' + str(e))

    def changeMethodSearch(self, QString):
        try:
            self.ui.lstMethodResult.clear()
            methodList = [x for x in info.currentMethodList if QString.lower() in x.lower()]

            info.mainUI.ui.lstMethodResult.setHorizontalHeaderLabels([''.join(['Name (', str(len(methodList)), ')'])])
            info.mainUI.ui.lstMethodResult.setRowCount(len(methodList))
            for i in range(len(methodList)):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setText(methodList[i])
                info.mainUI.ui.lstMethodResult.setItem(0, i, item)
            info.mainUI.ui.update()
        except Exception as e:
            print('[!] changeMethodSearch() Error : ' + str(e))



    #########################
    #   Enumerator - List   #
    #########################
    def clickListGo(self):
        try:
            if info.currentFilePath == '':
                return

            f = open(info.currentFilePath, 'r')
            data = f.read()
            f.close()

            self.ui.txtPlayScript_Edit.setPlainText(data.replace('\t', '    '))
            self.ui.tabWidget.setCurrentIndex(1)
        except Exception as e:
            print('[!] clickListGo() Error : ' + str(e))

    def clickListNew(self):
        try:
            reply = QInputDialog.getText(self, 'New File', 'Input New FileName', QLineEdit.Normal, '')
            if reply[1]:
                if not reply[0].endswith('.js'):
                    QMessageBox.warning(self, 'Warning', 'Only JavaScript File')
                    return
                selectItem = self.ui.treeScriptList.currentItem()
                filePath = selectPath(selectItem, reply[0])

                if os.path.exists(filePath):
                    reply = QMessageBox.question(self, 'Question', 'File already exists. Do you want to overwrite it?',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.No:
                        return

                f = open(filePath, 'w')
                f.close()
                self.ui.treeScriptList.clear()
                createFileSystem(default_File_path + 'User_script\\', self.ui.treeScriptList)
        except Exception as e:
            QMessageBox.warning(self, 'Warning', str(e))
            print('[!] clickListNew() Error : ' + str(e))

    def clickListSave(self):
        try:
            if self.ui.txtScriptEdit.isEnabled():
                data = self.ui.txtScriptEdit.toPlainText().replace('    ', '\t')
                f = open(info.currentFilePath, 'w')
                f.write(data)
                f.flush()
                f.close()
        except Exception as e:
            QMessageBox.warning(self, 'Warning', str(e))
            print('[!] clickListSave() Error : ' + str(e))

    def clickListSaveAs(self):
        try:
            if self.ui.txtScriptEdit.isEnabled():
                saveScript(self.ui.txtScriptEdit.toPlainText().replace('    ', '\t'), 1)
                self.ui.treeScriptList.clear()
                createFileSystem(default_File_path + 'User_script\\', self.ui.treeScriptList)
        except Exception as e:
            print('[!] clickListSaveAs() Error : ' + str(e))

    def clickListDelete(self):
        try:
            reply = QMessageBox.question(self, 'Question', 'Are you sure you want to delete it?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                selectItem = self.ui.treeScriptList.currentItem()
                filePath = getAbsPath(selectItem, 0)

                os.remove(filePath)
                self.ui.treeScriptList.clear()
                createFileSystem(default_File_path + 'User_script\\', self.ui.treeScriptList)
        except Exception as e:
            QMessageBox.warning(self, 'Warning', str(e))
            print('[!] clickListDelete() Error : ' + str(e))

    def clickListUpload(self):
        try:
            uploadForm = UploadForm(self)
            uploadForm.exec_()
        except Exception as e:
            QMessageBox.warning(self, 'Warning', str(e))
            print('[!] clickListUpload() Error : ' + str(e))

    def clickListDownLoad(self):
        try:
            downloadForm = DownloadForm(self)
            downloadForm.exec_()
        except Exception as e:
            QMessageBox.warning(self, 'Warning', str(e))
            print('[!] clickListDownLoad() Error : ' + str(e))

    def doubleScriptSelect(self, QTreeWidgetItem, index):
        self.ui.txtScriptEdit.setEnabled(True)
        try:
            if QTreeWidgetItem.text(index).endswith('.js'):
                filePath = getAbsPath(QTreeWidgetItem, index)

                f = open(filePath, "r")
                data = f.read()
                f.close()

                data = data.replace('\t', '    ')

                if filePath == default_File_path + QTreeWidgetItem.text(0):
                    self.ui.txtScriptEdit.setReadOnly(True)
                self.ui.txtScriptEdit.setPlainText(data)
                info.currentFilePath = filePath
        except Exception as e:
            QMessageBox.warning(self, 'Warning', str(e))
            print('[!] doubleScriptSelect() Error : ' + str(e))



    #####################
    #   Script Loader   #
    #####################
    def clickPlaySave(self):
        try:
            saveScript(self.ui.txtPlayScript_Edit.toPlainText().replace('    ', '\t'), 0)
        except Exception as e:
            print('[!] clickPlaySave() Error : ' + str(e))

    def clickPlayLoad(self):
        try:
            self.function_init()
            info.isPlay = True

            info.script_to_load = self.ui.txtPlayScript_Edit.toPlainText().replace('send(', 'send(\'ll00aaddll00aadd\'+')
            loadScript()

            self.timer = QTimer()
            self.timer.start(1000)
            self.timer.timeout.connect(self.playScript_timeout_run)
        except Exception as e:
            print('[-] clickPlayLoad() Error : ' + str(e))

    def clickPlayClear(self):
        try:
            self.ui.txtPlayScript_Result.clear()
            info.playResult = ''
        except Exception as e:
            print('[!] clickPlayClear() Error : ' + str(e))

    def clickPlayDetach(self):
        try:
            info.isPlay = False
            self.timer.stop()
            unloadScript()
        except Exception as e:
            print('[!] clickPlayDetach() Error : ' + str(e))

    def clickPlayExtract(self):
        try:
            extractContent(self.ui.txtPlayScript_Result.toPlainText())
        except Exception as e:
            print('[!] clickPlayExtract() Error : ' + str(e))




    ########################
    #    Implementation    #
    ########################
    def clickImplAdd(self):
        try:
            if info.implTemp.get('className') == None:
                info.implTemp['className'] = '?'
            if info.implTemp.get('methodName') == None:
                info.implTemp['methodName'] = '?'
            info.implTemp['script'] = self.ui.txtImpl_Function.toPlainText()
            impl_tmp = info.implTemp
            info.implCurrent.append(impl_tmp)

            self.ui.lstImpl_Current.setRowCount(info.implCount + 1)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(impl_tmp['className'])
            self.ui.lstImpl_Current.setItem(info.implCount, 0, item)

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(impl_tmp['methodName'])
            self.ui.lstImpl_Current.setItem(info.implCount, 1, item)

            item = QPushButton()
            item.setText('Detail')
            self.implButtonGroup.addButton(item, info.implCount)
            self.ui.lstImpl_Current.setCellWidget(info.implCount, 2, item)

            info.implCount += 1
            self.clickImplScript()
        except Exception as e:
            print('[-] clickImplAdd() Error : ' + str(e))

    def clickImplRemove(self):
        try:
            if info.implCount == 0:
                return
            selectRow = self.ui.lstImpl_Current.currentRow()

            self.ui.lstImpl_Current.removeRow(selectRow)
            self.ui.lstImpl_Current.setRowCount(info.implCount - 1)

            info.implCount -= 1
            info.implCurrent.pop(selectRow)
        except Exception as e:
            print('[-] clickImplRemove() Error : ' + str(e))

    def clickImplScript(self):
        try:
            info.implTemp = {}
            className = self.ui.txtImpl_ClassName.text()
            methodName = self.ui.txtImpl_MethodName.text()

            if className == '' or methodName == '':
                QMessageBox.information(self, 'Invalid', 'Please input className and methodName')
                return

            paramCount = len(methodName.split(':')) - 1
            paramStr = ''
            for i in range(paramCount):
                paramStr += ', arg' + str(i)
            renderScript(default_File_path + 'implementation_function.js', str(info.implCount), className, methodName, paramStr)

            f = open(default_File_path + 'implementation_function_tmp.js', 'r')
            data = f.read()
            f.close()
            os.remove(default_File_path + 'implementation_function_tmp.js')

            info.implTemp['className'] = className
            info.implTemp['methodName'] = methodName
            data = data.replace('\t', '    ')
            self.ui.txtImpl_Function.setPlainText(data)
        except Exception as e:
            print('[-] clickImplScript() Error : ' + str(e))

    def clickImplLoad(self):
        try:
            self.function_init()
            info.isImpl = True

            createImplScript()
            info.script_to_load = info.implScript.replace('send(', 'send(\'iimmppll22mm22nntt44ttii00nn\'+')
            loadScript()

            self.timer4 = QTimer()
            self.timer4.start(1000)
            self.timer4.timeout.connect(self.impl_timeout_run)
        except Exception as e:
            print('[-] clickImplLoad() Error : ' + str(e))

    def clickImplDetach(self):
        try:
            info.isImpl = False
            info.implScript = ''
            self.timer4.stop()
            unloadScript()
        except Exception as e:
            print('[-] clickImplDetach() Error : ' + str(e))

    def clickImplClear(self):
        try:
            self.ui.txtImpl_Log.clear()
            info.implResult = ''
        except Exception as e:
            print('[-] clickImplClear() Error : ' + str(e))

    def clickImplExtract(self):
        try:
            extractContent(self.ui.txtImpl_Log.toPlainText())
        except Exception as e:
            print('[-] clickImplExtract() Error : ' + str(e))

    def clickImpl_ButtonGroup(self, id):
        try:
            for button in self.implButtonGroup.buttons():
                if button is self.implButtonGroup.button(id):
                    detail = ''

                    detail += 'ClassName : ' + info.implCurrent[id]['className'] + '\n'
                    detail += 'MethodName : ' + info.implCurrent[id]['methodName'] + '\n'
                    detail += '\n[Script]\n'
                    detail += info.implCurrent[id]['script']

                    QMessageBox.information(self, 'Detail Information', detail)
        except Exception as e:
            print('[-] clickImpl_ButtonGroup() Error : ' + str(e))



    ###################
    #   Interceptor   #
    ###################
    def changeInterceptorType(self, QString):
        try:
            if QString == 'Log':
                self.ui.txtInterceptor_ret.setEnabled(False)
                numOfEnable(0)
                info.interceptType = 'Log'
            elif QString == 'Replace':
                self.ui.txtInterceptor_ret.setEnabled(True)
                self.ui.comboInterceptor_returnType.setEnabled(True)
                numOfEnable(int(self.ui.comboInterceptor_argNum.currentText()))
                info.interceptType = 'Replace'
        except Exception as e:
            print('[!] changeInterceptorType() Error : ' + str(e))

    def changeInterceptorArgNum(self, QString):
        try:
            if info.interceptType == 'Replace':
                numOfEnable(int(QString))
        except Exception as e:
            print('[!] changeInterceptorArgNum() Error : ' + str(e))

    def changeInterceptorMethodName(self):
        try:
            if not self.ui.txtInterceptor_MethodName.text().endswith(':'):
                self.ui.comboInterceptor_argNum.setCurrentIndex(0)
                return

            argNum = len(self.ui.txtInterceptor_MethodName.text().split(':')) - 1
            if argNum > 8:
                return
            self.ui.comboInterceptor_argNum.setCurrentIndex(argNum)
        except Exception as e:
            print('[!] changeInterceptorMethodName() Error : ' + str(e))

    def clickInterceptorClassMethod(self):
        try:
            if info.isOffset == False:
                return
            self.ui.txtInterceptor_ClassName.setEnabled(True)
            self.ui.txtInterceptor_MethodName.setEnabled(True)

            self.ui.txtInterceptor_Offset.setText('')
            self.ui.txtInterceptor_Offset.setEnabled(False)
            info.isOffset = False

            self.ui.comboInterceptor_argNum.setCurrentIndex(0)
            self.ui.comboInterceptor_argNum.setEnabled(False)
        except Exception as e:
            print('[!] clickInterceptorClassMethod() Error : ' + str(e))

    def clickInterceptorOffset(self):
        try:
            if info.isOffset == True:
                return
            QMessageBox.warning(self, 'Information', 'Offset 으로 Interceptor를 설정할 경우,\nReturn Type이 Boolean/Int형인 경우에만 Replace할 수 있습니다!!')
            self.ui.txtInterceptor_ClassName.setText('')
            self.ui.txtInterceptor_ClassName.setEnabled(False)
            self.ui.txtInterceptor_MethodName.setText('')
            self.ui.txtInterceptor_MethodName.setEnabled(False)

            self.ui.txtInterceptor_Offset.setEnabled(True)
            info.isOffset = True

            self.ui.comboInterceptor_argNum.setEnabled(True)
        except Exception as e:
            print('[!] clickInterceptorOffset() Error : ' + str(e))

    def clickInterceptorAdd(self):
        if info.isOffset == False and (self.ui.txtInterceptor_ClassName.text() == '' or self.ui.txtInterceptor_MethodName.text() == ''):
            return
        if info.isOffset == True and self.ui.txtInterceptor_Offset.text() == '':
            return
        try:
            data = {}

            # self.ui.txtInterceptor_ClassName
            # self.ui.txtInterceptor_MethodName
            for i in range(self.ui.lstInterceptor_Current.rowCount()):
                if (self.ui.txtInterceptor_ClassName.text() == self.ui.lstInterceptor_Current.item(i, 0).text()) and (self.ui.txtInterceptor_MethodName.text() == self.ui.lstInterceptor_Current.item(i, 1).text()):
                    QMessageBox.warning(self, 'Warning', 'Already Intercept Class/Method')
                    return

            self.ui.lstInterceptor_Current.setRowCount(info.interceptCount + 1)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            if info.isOffset == True:
                item.setText('NULL')
                data['className'] = 'NULL'
            else:
                item.setText(self.ui.txtInterceptor_ClassName.text())
                data['className'] = self.ui.txtInterceptor_ClassName.text()
            print(data['className'])
            self.ui.lstInterceptor_Current.setItem(info.interceptCount, 0, item)

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            if info.isOffset == True:
                item.setText(self.ui.txtInterceptor_Offset.text())
                data['methodName'] = self.ui.txtInterceptor_Offset.text()
            else:
                item.setText(self.ui.txtInterceptor_MethodName.text())
                data['methodName'] = self.ui.txtInterceptor_MethodName.text()
            self.ui.lstInterceptor_Current.setItem(info.interceptCount, 1, item)

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(self.ui.comboInterceptor_Type.currentText())
            data['type'] = self.ui.comboInterceptor_Type.currentText()
            self.ui.lstInterceptor_Current.setItem(info.interceptCount, 2, item)

            item = QPushButton()
            item.setText('Detail')
            self.interceptorButtonGroup.addButton(item, info.interceptCount)
            self.ui.lstInterceptor_Current.setCellWidget(info.interceptCount, 3, item)

            data['argc'] = self.ui.comboInterceptor_argNum.currentText()
            if data['type'] == 'Replace':
                for i in range(int(data['argc'])):
                    data[i] = eval('self.ui.txtInterceptor_arg' + str(i) + '.text()')
                data['retval'] = self.ui.txtInterceptor_ret.text()

            info.interceptCurrent.append(data)
            info.interceptCount += 1
        except Exception as e:
            print('[-] clickInterceptorAdd() Error : ' + str(e))

    def clickInterceptorRemove(self):
        try:
            if info.interceptCount == 0:
                return
            selectRow = self.ui.lstInterceptor_Current.currentRow()

            self.ui.lstInterceptor_Current.removeRow(selectRow)
            self.ui.lstInterceptor_Current.setRowCount(info.interceptCount - 1)
            info.interceptCount -= 1

            info.interceptCurrent.pop(selectRow)
        except Exception as e:
            print('[!] clickInterceptorRemove() Error : ' + str(e))

    def clickInterceptor_ButtonGroup(self, id):
        try:
            for button in self.interceptorButtonGroup.buttons():
                if button is self.interceptorButtonGroup.button(id):
                    detail = ''

                    detail += 'ClassName : ' + info.interceptCurrent[id]['className'] + '\n'
                    detail += 'MethodName : ' + info.interceptCurrent[id]['methodName'] + '\n'
                    detail += 'Type : ' + info.interceptCurrent[id]['type'] + '\n'
                    detail += 'Argument Number : ' + info.interceptCurrent[id]['argc'] + '\n'
                    for i in range(int(info.interceptCurrent[id]['argc'])):
                        detail += 'Arg' + str(i) + ' : ' + info.interceptCurrent[id][i] + '\n'
                    if info.interceptCurrent[id]['type'] == 'Replace':
                        detail += 'Return Value : ' + info.interceptCurrent[id]['retval'] + '\n'

                    QMessageBox.information(self, 'Detail Information', detail)
        except Exception as e:
            print('[-] clickInterceptor_ButtonGroup() Error : ' + str(e))

    def clickInterceptorLoad(self):
        try:
            self.function_init()
            info.isIntercept = True

            createInterceptScript()
            info.script_to_load = info.interceptScript.replace('send(', 'send(\'iinntt22rrcc22pptt\'+')
            loadScript()

            self.timer2 = QTimer()
            self.timer2.start(1000)
            self.timer2.timeout.connect(self.intercept_timeout_run)
        except Exception as e:
            print('[-] clickInterceptorLoad() Error : ' + str(e))

    def clickInterceptorDetach(self):
        try:
            info.isIntercept = False
            self.timer2.stop()
            info.interceptScript = ''
            unloadScript()
        except Exception as e:
            print('[!] clickInterceptorDetach() Error : ' + str(e))

    def clickInterceptorRemoveAll(self):
        try:
            info.interceptCount = 0
            info.interceptCurrent = []
            self.ui.lstInterceptor_Current.setRowCount(0)
            info.interceptScript = ''
        except Exception as e:
            print('[!] clickInterceptorRemoveAll() Error : ' + str(e))

    def clickInterceptorClear(self):
        try:
            info.interceptResult = ''
            self.ui.txtInterceptor_Log.setPlainText('')
        except Exception as e:
            print('[!] clickInterceptorClear() Error : ' + str(e))

    def clickInterceptorExtract(self):
        try:
            extractContent(self.ui.txtInterceptor_Log.toPlainText())
        except Exception as e:
            print('[!] clickInterceptorExtract() Error : ' + str(e))




    ################
    #   Debugger   #
    ################
    # Debugger Detach시 프로세스를 종료하도록 했다. 왜냐하면 나머지 기능에 영향을 미치기 때문이다.
    # Debugger Script를 unload한 이후 unload작업에서 15~20초정도가 매번 소요되는 현상을 해결할 방법을 찾지 못했다.
    # Debugger를 동작시키고 다른 기능을 동작시켜서는 안되고, 반드시 Detach하고 넘어가도록 한다.
    def clickDebugAdd(self):
        try:
            if self.ui.txtDebug_Address.text() == '':
                QMessageBox.warning(self, 'Warning', 'First Input Address')
                return

            match = re.search(r'^0x(?:[0-9a-fA-F]+)$', self.ui.txtDebug_Address.text())
            if not match:
                QMessageBox.warning(self, 'Warning', 'Input Format is 0x123456')
                return

            for i in range(self.ui.lstDebug_BPAddress.rowCount()):
                if (self.ui.txtDebug_Address.text() == self.ui.lstDebug_BPAddress.item(i, 0).text()):
                    QMessageBox.warning(self, 'Warning', 'Already Debugging Address')
                    return

            self.ui.lstDebug_BPAddress.setRowCount(info.debugCount + 1)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(self.ui.txtDebug_Address.text())
            self.ui.lstDebug_BPAddress.setItem(info.debugCount, 0, item)

            self.ui.txtDebug_Address.clear()
            info.debugCount += 1
        except Exception as e:
            print('[-] clickDebugAdd() Error : ' + str(e))

    def clickDebugDelete(self):
        try:
            if info.debugCount == 0:
                return
            killProcess()
            selectRow = self.ui.lstDebug_BPAddress.currentRow()

            self.ui.lstDebug_BPAddress.removeRow(selectRow)
            self.ui.lstDebug_BPAddress.setRowCount(info.debugCount - 1)

            info.debugCount -= 1
        except Exception as e:
            print('[-] clickDebugDelete() Error : ' + str(e))

    def clickDebugClear(self):
        try:
            killProcess()
            self.ui.lstDebug_BPAddress.setRowCount(0)
            info.debugCount = 0
        except Exception as e:
            print('[-] clickDebugClear() Error : ' + str(e))

    def clickDebugLoad(self):
        try:
            self.function_init()
            info.isDebug = True

            createDebugScript()
            info.script_to_load = info.debugScript.replace('send(', 'send(\'dd22bbuu99\'+')
            loadScript()
        except Exception as e:
            print('[-] clickDebugLoad() Error : ' + str(e))

    def clickDebugDetach(self):
        try:
            info.debugScript = ''
            killProcess()

            self.ui.txtDebug_CurrentAddress.setText('')
            self.ui.txtDebug_x0.setText('')
            self.ui.txtDebug_x1.setText('')
            self.ui.txtDebug_x2.setText('')
            self.ui.txtDebug_x3.setText('')
            self.ui.txtDebug_x4.setText('')
            self.ui.txtDebug_x5.setText('')
            self.ui.txtDebug_x6.setText('')
            self.ui.txtDebug_x7.setText('')
            self.ui.txtDebug_x8.setText('')
            self.ui.txtDebug_x9.setText('')
            self.ui.txtDebug_x10.setText('')
            self.ui.txtDebug_x11.setText('')
            self.ui.txtDebug_x12.setText('')
            self.ui.txtDebug_x13.setText('')
            self.ui.txtDebug_x14.setText('')
            self.ui.txtDebug_x15.setText('')
            self.ui.txtDebug_x16.setText('')
            self.ui.txtDebug_x17.setText('')
            self.ui.txtDebug_x18.setText('')
            self.ui.txtDebug_x19.setText('')
            self.ui.txtDebug_x20.setText('')
            self.ui.txtDebug_x21.setText('')
            self.ui.txtDebug_x22.setText('')
            self.ui.txtDebug_x23.setText('')
            self.ui.txtDebug_x24.setText('')
            self.ui.txtDebug_x25.setText('')
            self.ui.txtDebug_x26.setText('')
            self.ui.txtDebug_x27.setText('')
            self.ui.txtDebug_x28.setText('')
            self.ui.txtDebug_x29.setText('')
            self.ui.txtDebug_BaseAddress.setText('')
        except Exception as e:
            print('[-] clickDebugDetach() Error : ' + str(e))

    def clickDebugContinue(self):
        try:
            info.script.post({'x0': self.ui.txtDebug_x0.text(),
                              'x1': self.ui.txtDebug_x1.text(),
                              'x2': self.ui.txtDebug_x2.text(),
                              'x3': self.ui.txtDebug_x3.text(),
                              'x4': self.ui.txtDebug_x4.text(),
                              'x5': self.ui.txtDebug_x5.text(),
                              'x6': self.ui.txtDebug_x6.text(),
                              'x7': self.ui.txtDebug_x7.text(),
                              'x8': self.ui.txtDebug_x8.text(),
                              'x9': self.ui.txtDebug_x9.text(),
                              'x10': self.ui.txtDebug_x10.text(),
                              'x11': self.ui.txtDebug_x11.text(),
                              'x12': self.ui.txtDebug_x12.text(),
                              'x13': self.ui.txtDebug_x13.text(),
                              'x14': self.ui.txtDebug_x14.text(),
                              'x15': self.ui.txtDebug_x15.text(),
                              'x16': self.ui.txtDebug_x16.text(),
                              'x17': self.ui.txtDebug_x17.text(),
                              'x18': self.ui.txtDebug_x18.text(),
                              'x19': self.ui.txtDebug_x19.text(),
                              'x20': self.ui.txtDebug_x20.text(),
                              'x21': self.ui.txtDebug_x21.text(),
                              'x22': self.ui.txtDebug_x22.text(),
                              'x23': self.ui.txtDebug_x23.text(),
                              'x24': self.ui.txtDebug_x24.text(),
                              'x25': self.ui.txtDebug_x25.text(),
                              'x26': self.ui.txtDebug_x26.text(),
                              'x27': self.ui.txtDebug_x27.text(),
                              'x28': self.ui.txtDebug_x28.text(),
                              'lr': self.ui.txtDebug_x29.text()})
            self.ui.txtDebug_CurrentAddress.setText('')
            self.ui.txtDebug_BaseAddress.setText('')
            self.ui.txtDebug_x0.setText('')
            self.ui.txtDebug_x1.setText('')
            self.ui.txtDebug_x2.setText('')
            self.ui.txtDebug_x3.setText('')
            self.ui.txtDebug_x4.setText('')
            self.ui.txtDebug_x5.setText('')
            self.ui.txtDebug_x6.setText('')
            self.ui.txtDebug_x7.setText('')
            self.ui.txtDebug_x8.setText('')
            self.ui.txtDebug_x9.setText('')
            self.ui.txtDebug_x10.setText('')
            self.ui.txtDebug_x11.setText('')
            self.ui.txtDebug_x12.setText('')
            self.ui.txtDebug_x13.setText('')
            self.ui.txtDebug_x14.setText('')
            self.ui.txtDebug_x15.setText('')
            self.ui.txtDebug_x16.setText('')
            self.ui.txtDebug_x17.setText('')
            self.ui.txtDebug_x18.setText('')
            self.ui.txtDebug_x19.setText('')
            self.ui.txtDebug_x20.setText('')
            self.ui.txtDebug_x21.setText('')
            self.ui.txtDebug_x22.setText('')
            self.ui.txtDebug_x23.setText('')
            self.ui.txtDebug_x24.setText('')
            self.ui.txtDebug_x25.setText('')
            self.ui.txtDebug_x26.setText('')
            self.ui.txtDebug_x27.setText('')
            self.ui.txtDebug_x28.setText('')
            self.ui.txtDebug_x29.setText('')
        except Exception as e:
            print('[-] clickDebugContinue() Error : ' + str(e))



    #####################
    #   Memory - Scan   #
    #####################
    def clickMemoryMaps(self):
        try:
            info.memoryMapsCount = 0;
            self.ui.lstMemoryScan_Address.setRowCount(0)

            f = open(default_File_path + "memoryMaps.js", "r")
            data = f.read()
            info.script_to_load = data.replace('send(', 'send(\'mm44pp22\'+')
            loadScript()
        except Exception as e:
            print('[!] clickMemoryMaps() Error : ' + str(e))

    def clickMemoryAll(self):
        try:
            selectedIndexList = [i.row() for i in self.ui.lstMemoryScan_Address.selectedItems()]
            for i in range(0, info.memoryMapsCount):
                if i not in selectedIndexList:
                    self.ui.lstMemoryScan_Address.selectRow(i)
        except Exception as e:
            print('[!] clickMemoryAll() Error : ' + str(e))

    def clickMemoryReset(self):
        try:
            selectedIndexList = [i.row() for i in self.ui.lstMemoryScan_Address.selectedItems()]
            for i in range(0, info.memoryMapsCount):
                if i in selectedIndexList:
                    self.ui.lstMemoryScan_Address.selectRow(i)
        except Exception as e:
            print('[!] clickMemoryReset() Error : ' + str(e))

    def clickMemoryScan(self):
        try:
            self.ui.MemoryStack.setCurrentIndex(0)
            self.ui.lstMemoryScan_Address.setSelectionMode(QAbstractItemView.MultiSelection)
        except Exception as e:
            print('[!] clickMemoryScan() Error : ' + str(e))

    def clickMemoryDumpPage(self):
        try:
            self.ui.MemoryStack.setCurrentIndex(1)
            self.clickMemoryReset()
            self.ui.lstMemoryScan_Address.setSelectionMode(QAbstractItemView.SingleSelection)
        except Exception as e:
            print('[!] clickMemoryScan() Error : ' + str(e))

    def clickMemoryPatch(self):
        try:
            self.ui.MemoryStack.setCurrentIndex(2)
            self.ui.lstMemoryScan_Address.setSelectionMode(QAbstractItemView.MultiSelection)
        except Exception as e:
            print('[!] clickMemoryPatch() Error : ' + str(e))

    def clickMemoryScanStart(self):
        try:
            if self.ui.txtMemoryScan_input.text() == '':
                return

            searchData = self.ui.txtMemoryScan_input.text()
            if self.ui.comboMemoryScan_type.currentText() == 'String':
                searchData = str2hex(searchData)
            if not memoryScanTypeCheck(searchData, 'Hex'):
                QMessageBox.warning(self, "Warning", "Input Data is not valid!!")
                return

            self.function_init()

            result_lst = []
            for i in range(0, len(self.ui.lstMemoryScan_Address.selectedItems()), 2):
                tmp_lst = [self.ui.lstMemoryScan_Address.selectedItems()[i].text(), self.ui.lstMemoryScan_Address.selectedItems()[i + 1].text()]
                result_lst.append(tmp_lst)
            renderScript(default_File_path + 'memoryScan.js', searchData, str(int(self.ui.numMemoryScan_scope.text()) * 16), str((int(self.ui.numMemoryScan_scope.text()) * 2 + 1) * 16), str(result_lst))

            f = open(default_File_path + "memoryScan_tmp.js", "r")
            data = f.read()
            f.close()
            os.remove(default_File_path + "memoryScan_tmp.js")

            info.script_to_load = data.replace('send(', 'send(\'mm22mmsscc44nn\'+')
            loadScript()
        except Exception as e:
            print('[!] clickMemoryScanStart() Error : ' + str(e))

    def clickMemoryScanStop(self):
        try:
            unloadScript()
            info.script_to_load = ''
            info.memoryCount = 0
        except Exception as e:
            print('[!] clickMemoryScanStop() Error : ' + str(e))

    def clickMemoryScanClear(self):
        try:
            self.ui.lstMemoryScan_Result.setRowCount(0)
            info.memoryCount = 0
            info.memoryResult.clear()
        except Exception as e:
            print('[!] clickMemoryScanClear() Error : ' + str(e))

    def clickMemoryScanExtract(self):
        try:
            data = ''
            for i in info.memoryResult:
                data += i + '\n\n'
            extractContent(data)
        except Exception as e:
            print('[!] clickMemoryScanExtract() Error : ' + str(e))



    #####################
    #   Memory - Dump   #
    #####################
    def clickMemoryPath(self):
        try:
            fname = QFileDialog.getExistingDirectory(self, "Get Directory Path", default_Output_path)
            self.ui.txtMemoryDump_path.setText(fname + "\\Dump\\")
        except Exception as e:
            print('[!] clickMemoryPath() Error : ' + str(e))

    def changeMemoryDumpStartAddress(self):
        try:
            if self.ui.txtMemoryDump_start.text() == '':
                return

            match = re.search(r'^0x(?:[0-9a-fA-F]+)$', self.ui.txtMemoryDump_start.text())
            if not match:
                QMessageBox.warning(self, 'Warning', 'Input Format of Start Address is 0x123456')
                self.ui.txtMemoryDump_start.clear()
                self.ui.txtMemoryDump_start.setFocus()
                return

            if self.ui.txtMemoryDump_end.text() == '':
                return

            start_address = int(self.ui.txtMemoryDump_start.text(), 16)
            end_address = int(self.ui.txtMemoryDump_end.text(), 16)

            if end_address - start_address + 1 > 0:
                self.ui.txtMemoryDump_len.setText(str(end_address - start_address + 1))
            else:
                QMessageBox.warning(self, 'Warning', 'Set Start Address Smaller Then Endd Address')
                self.ui.txtMemoryDump_start.setFocus()
                return
        except Exception as e:
            print('[!] changeMemoryStartAddress() Error : ' + str(e))

    def changeMemoryDumpEndAddress(self):
        try:
            if self.ui.txtMemoryDump_end.text() == '':
                return

            match = re.search(r'^0x(?:[0-9a-fA-F]+)$', self.ui.txtMemoryDump_end.text())
            if not match:
                QMessageBox.warning(self, 'Warning', 'Input Format of End Address is 0x123456')
                self.ui.txtMemoryDump_end.clear()
                self.ui.txtMemoryDump_end.setFocus()
                return

            if self.ui.txtMemoryDump_start.text() == '':
                return

            start_address = int(self.ui.txtMemoryDump_start.text(), 16)
            end_address = int(self.ui.txtMemoryDump_end.text(), 16)

            if end_address - start_address + 1 > 0:
                self.ui.txtMemoryDump_len.setText(str(end_address - start_address + 1))
            else:
                QMessageBox.warning(self, 'Warning', 'Set End Address Bigger Then Start Address')
                self.ui.txtMemoryDump_end.setFocus()
                return
        except Exception as e:
            print('[!] changeMemoryEndAddress() Error : ' + str(e))

    def clickMemoryDump(self):
        try:
            if self.ui.txtMemoryDump_start.text() == '':
                QMessageBox.warning(self.ui, 'Failed', 'Please input start address!')
                return
            match = re.search(r'^0x(?:[0-9a-fA-F]+)$', self.ui.txtMemoryDump_start.text())
            if not match:
                QMessageBox.warning(self, 'Warning', 'Input Format of Start Address is 0x123456')
                return

            if self.ui.txtMemoryDump_len.text() == '':
                QMessageBox.warning(self.ui, 'Failed', 'Please input address length!')
                return
            match = re.search(r'^(?:[0-9]*)$', self.ui.txtMemoryDump_len.text())
            if not match:
                QMessageBox.warning(self, 'Warning', 'Input Format of Length is 123456')
                return

            if not os.path.exists(self.ui.txtMemoryDump_path.text()):
                os.mkdir(self.ui.txtMemoryDump_path.text())

            start = int(self.ui.txtMemoryDump_start.text(), 16)
            len = int(self.ui.txtMemoryDump_len.text())
            max_size = 20971520

            f = open(default_File_path + "memoryDump.js", "r")
            data = f.read()
            f.close()

            self.function_init()
            info.script_to_load = data
            loadScript()
            exports = info.script.exports

            count = len // max_size
            mod = len % max_size

            for i in range(count):
                self.dump_to_file(exports, start + (max_size * i), max_size)
            self.dump_to_file(exports, start + (max_size * count), mod)

            unloadScript()
        except Exception as e:
            print('[!] clickMemoryDump() Error : ' + str(e))

    def dump_to_file(self, exports, base, size):
        try:
            filename = str(hex(base)) + '_dump.data'
            dump = exports.read_memory(base, size)
            f = open(self.ui.txtMemoryDump_path.text() + filename, 'wb')
            f.write(dump)
            f.close()

            log = 'Start Address: ' + str(hex(base)) + ', Length: ' + str(size) + '\n'
            log += 'Create File: ' + self.ui.txtMemoryDump_path.text() + filename + '\n'
            log += 'Success!!' + '\n'
            print(log)
            self.ui.txtMemoryDump_Log.setPlainText(self.ui.txtMemoryDump_Log.toPlainText() + log + '\n')
        except Exception as e:
            print("Oops, memory access violation!")

            log = 'Start Address: ' + str(hex(base)) + ', Length: ' + str(size) + '\n'
            log += 'Create File: ' + self.ui.txtMemoryDump_path.text() + filename + '\n'
            log += 'Failed!! Memory Access Violation!!' + '\n'
            print(log)
            self.ui.txtMemoryDump_Log.setPlainText(self.ui.txtMemoryDump_Log.toPlainText() + log + '\n')

    def clickMemoryDumpClear(self):
        try:
            self.ui.txtMemoryDump_Log.clear()
        except Exception as e:
            print('[!] clickMemoryDumpClear() Error : ' + str(e))



    #####################
    #   Memory - Patch  #
    #####################
    def changeMemoryPatchStartAddress(self):
        try:
            if self.ui.txtMemoryPatch_start.text() == '':
                return

            match = re.search(r'^0x(?:[0-9a-fA-F]+)$', self.ui.txtMemoryPatch_start.text())
            if not match:
                QMessageBox.warning(self, 'Warning', 'Input Format of Start Address is 0x123456')
                self.ui.txtMemoryPatch_start.clear()
                self.ui.txtMemoryPatch_start.setFocus()
                return

            if self.ui.txtMemoryPatch_end.text() == '':
                return

            start_address = int(self.ui.txtMemoryPatch_start.text(), 16)
            end_address = int(self.ui.txtMemoryPatch_end.text(), 16)

            if end_address - start_address + 1 > 0:
                self.ui.txtMemoryPatch_len.setText(str(end_address - start_address + 1))
            else:
                QMessageBox.warning(self, 'Warning', 'Set Start Address Smaller Then Endd Address')
                self.ui.txtMemoryPatch_start.setFocus()
                return
        except Exception as e:
            print('[!] changeMemoryPatchStartAddress() Error : ' + str(e))

    def changeMemoryPatchEndAddress(self):
        try:
            if self.ui.txtMemoryPatch_end.text() == '':
                return

            match = re.search(r'^0x(?:[0-9a-fA-F]+)$', self.ui.txtMemoryPatch_end.text())
            if not match:
                QMessageBox.warning(self, 'Warning', 'Input Format of End Address is 0x123456')
                self.ui.txtMemoryPatch_end.clear()
                self.ui.txtMemoryPatch_end.setFocus()
                return

            if self.ui.txtMemoryPatch_start.text() == '':
                return

            start_address = int(self.ui.txtMemoryPatch_start.text(), 16)
            end_address = int(self.ui.txtMemoryPatch_end.text(), 16)

            if end_address - start_address + 1 > 0:
                self.ui.txtMemoryPatch_len.setText(str(end_address - start_address + 1))
            else:
                QMessageBox.warning(self, 'Warning', 'Set End Address Bigger Then Start Address')
                self.ui.txtMemoryPatch_end.setFocus()
                return
        except Exception as e:
            print('[!] changeMemoryPatchEndAddress() Error : ' + str(e))

    def changeMemoryPatchSearch(self):
        try:
            if self.ui.txtMemoryPatch_search.text() == '':
                return

            searchData = self.ui.txtMemoryPatch_search.text()
            if self.ui.comboMemoryPatch_type.currentText() == 'String':
                searchData = str2hex(searchData)
            if not memoryScanTypeCheck(searchData, 'Hex'):
                QMessageBox.warning(self, "Warning", "Input Data is not valid!!")
                self.ui.txtMemoryPatch_search.setFocus()
                return
        except Exception as e:
            print('[!] changeMemoryPatchSearch() Error : ' + str(e))

    def clickMemoryPatchReplace(self):
        try:
            if self.ui.txtMemoryPatch_start.text() == '' or \
                    self.ui.txtMemoryPatch_len.text() == '' or \
                    self.ui.txtMemoryPatch_search.text() == '':
                return

            searchData = self.ui.txtMemoryPatch_search.text()
            if self.ui.comboMemoryPatch_type.currentText() == 'String':
                searchData = str2hex(searchData)

            renderScript(default_File_path + "memoryPatch.js", self.ui.txtMemoryPatch_start.text(), self.ui.txtMemoryPatch_len.text(), str(['0x' + i for i in searchData.split()]))
            f = open(default_File_path + "memoryPatch_tmp.js", 'r')
            data = f.read()
            f.close()

            self.function_init()
            info.script_to_load = data
            loadScript()
        except Exception as e:
            print('[!] clickMemoryPatchReplace() Error : ' + str(e))

    def clickMemoryPatchReplaceAll(self):
        try:
            if self.ui.txtMemoryPatchAll_before.text() == '' or \
                    self.ui.txtMemoryPatchAll_after.text() == '':
                return

            if len(self.ui.txtMemoryPatchAll_before.text()) != len(self.ui.txtMemoryPatchAll_after.text()):
                QMessageBox.warning(self, "Warning", "Before and After must be the same length!!")
                self.ui.txtMemoryPatchAll_before.setFocus()
                return

            beforeData = str2hex(self.ui.txtMemoryPatchAll_before.text())
            afterData = str2hex(self.ui.txtMemoryPatchAll_after.text())

            result_lst = []
            for i in range(0, len(self.ui.lstMemoryScan_Address.selectedItems()), 2):
                tmp_lst = [self.ui.lstMemoryScan_Address.selectedItems()[i].text(),
                           self.ui.lstMemoryScan_Address.selectedItems()[i + 1].text()]
                result_lst.append(tmp_lst)

            renderScript(default_File_path + "memoryPatchAll.js", beforeData, str(result_lst), str(['0x' + i for i in afterData.split()]))
            f = open(default_File_path + "memoryPatchAll_tmp.js", 'r')
            data = f.read()
            f.close()

            self.function_init()
            info.isMemPatch = True

            self.timer5 = QTimer()
            self.timer5.start(1000)
            self.timer5.timeout.connect(self.memory_patch_timeout_run)

            info.script_to_load = data.replace('send(', 'send(\'rr22pp1144cc2244llll\'+')
            loadScript()
        except Exception as e:
            print('[!] clickMemoryPatchReplaceAll() Error : ' + str(e))

    def clickMemoryPatchDetach(self):
        try:
            self.timer5.stop()
            info.isMemPatch = False
            unloadScript()
        except Exception as e:
            print('[!] clickMemoryPatchDetach() Error : ' + str(e))

    def clickMemoryPatchClear(self):
        try:
            info.memoryPatchResult = ''
            self.ui.txtMemoryPatch_Log.clear()
        except Exception as e:
            print('[!] clickMemoryPatchClear() Error : ' + str(e))

    def clickMemoryPatchExtract(self):
        try:
            extractContent(self.ui.txtMemoryPatch_Log.toPlainText())
        except Exception as e:
            print('[!] clickMemoryPatchExtract() Error : ' + str(e))



    #################
    #   API Trace   #
    #################
    def clickTraceAdd(self):
        try:
            new_filter = self.ui.txtTrace_Filter.text()
            if new_filter == '*[* *]':
                QMessageBox.warning(self, 'Warning', 'Invalid Filtering!!')
                return;

            regex = re.compile('exports:.*!.*')
            mc = regex.search(new_filter)
            if mc == None:
                regex = re.compile('.*\[.* .*\]')
                mc = regex.search(new_filter)
                if mc == None:
                    QMessageBox.warning(self, 'Warning', 'Invalid Filtering!!')
                    return;

            self.ui.lstTrace_Filters.setRowCount(info.TraceFilterCount + 1)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(new_filter)
            self.ui.lstTrace_Filters.setItem(info.TraceFilterCount, 0, item)

            info.TraceFilterCount += 1
        except Exception as e:
            print('[-] clickTraceAdd() Error : ' + str(e))

    def clickTraceRemove(self):
        try:
            if info.TraceFilterCount == 0:
                return
            selectRow = self.ui.lstTrace_Filters.currentRow()

            self.ui.lstTrace_Filters.removeRow(selectRow)
            self.ui.lstTrace_Filters.setRowCount(info.TraceFilterCount - 1)
            info.TraceFilterCount -= 1
        except Exception as e:
            print('[-] clickTraceRemove() Error : ' + str(e))

    def clickTraceStart(self):
        try:
            self.function_init()
            info.isTrace = True

            info.traceScript = ''
            info.traceResult = []
            info.traceSearchResult = []
            info.traceCount = 0

            createTraceScript()
            info.script_to_load = info.traceScript.replace('send(', 'send(\'ttrr44cc22\'+')
            loadScript()

            self.timer3 = QTimer()
            self.timer3.start(1000)
            self.timer3.timeout.connect(self.trace_timeout_run)

            self.ui.labelTrace_Status.setText('Running...')
            self.ui.labelTrace_Status.setStyleSheet('Color: Green')
        except Exception as e:
            print('[-] clickTraceStart() Error : ' + str(e))

    def clickTraceDetach(self):
        try:
            self.timer3.stop()

            info.traceScript = ''
            info.traceResult = []
            info.traceSearchResult = []
            info.traceCount = 0
            unloadScript()

            self.ui.labelTrace_Status.setText('Stop')
            self.ui.labelTrace_Status.setStyleSheet('Color: Black')
        except Exception as e:
            print('[-] clickTraceDetach() Error : ' + str(e))

    def clickTraceContinue(self):
        try:
            if info.traceScript == '':
                return
            info.isTrace = True
            self.ui.labelTrace_Status.setText('Running...')
            self.ui.labelTrace_Status.setStyleSheet('Color: Green')
        except Exception as e:
            print('[-] clickTraceContinue() Error : ' + str(e))

    def clickTraceStop(self):
        try:
            info.isTrace = False
            self.ui.labelTrace_Status.setText('Pause')
            self.ui.labelTrace_Status.setStyleSheet('Color: Red')
        except Exception as e:
            print('[-] clickTraceStop() Error : ' + str(e))

    def clickTraceClear(self):
        try:
            self.ui.txtTrace_Result.setPlainText('')
            info.traceResult = []
            info.traceSearchResult = []
            info.traceCount = 0
        except Exception as e:
            print('[-] clickTraceClear() Error : ' + str(e))

    def clickTraceExtract(self):
        try:
            extractContent(self.ui.txtTrace_Result.toPlainText())
        except Exception as e:
            print('[-] clickTraceExtract() Error : ' + str(e))

    def clickTraceHelp(self):
        try:
            QMessageBox.information(self, 'Help', '            <Example>\n*[*ClassName* *MethodName*]\n+[ClassName* *]\nexports:libSystem.B.dylib!open\nexports:*!open\n\n(*[* *] is not correct!)')
        except Exception as e:
            print('[-] clickTraceHelp() Error : ' + str(e))

    def changeTraceSearch(self, QString):
        try:
            info.traceSearchResult.clear()
            for str in info.traceResult:
                if QString.lower() in str.lower():
                    info.traceSearchResult.append(str)
        except Exception as e:
            print('[-] changeTraceSearch() Error : ' + str(e))


    ##################
    #   TimeoutRun   #
    ##################
    def playScript_timeout_run(self):
        try:
            if info.isPlay:
                print('call playScript_timeout_run')
                self.ui.txtPlayScript_Result.setPlainText(info.playResult)
                self.ui.txtPlayScript_Result.moveCursor(QTextCursor.End)
        except Exception as e:
            print('[!] playScript_timeout_run() Error : ' + str(e))

    def intercept_timeout_run(self):
        try:
            if info.isIntercept:
                print('call intercept_timeout_run')
                self.ui.txtInterceptor_Log.setPlainText(info.interceptResult)
                self.ui.txtInterceptor_Log.moveCursor(QTextCursor.End)
        except Exception as e:
            print('[!] intercept_timeout_run() Error : ' + str(e))

    def trace_timeout_run(self):
        try:
            if info.isTrace:
                self.ui.txtTrace_Result.setTextColor(QColor(0, 0, 0))
                self.ui.txtTrace_Result.clear()
                print('call trace_timeout_run')

                for i in range(len(info.traceSearchResult)):
                    if info.traceSearchResult[i].lstrip().find('[+]') != -1 or info.traceSearchResult[i].lstrip().find('[-]') != -1:
                        self.ui.txtTrace_Result.setTextColor(QColor(255, 0, 0))
                    self.ui.txtTrace_Result.append(info.traceSearchResult[i])
                    self.ui.txtTrace_Result.setTextColor(QColor(0, 0, 0))
        except Exception as e:
            print('[!] trace_timeout_run() Error : ' + str(e))

    def impl_timeout_run(self):
        try:
            if info.isImpl:
                print('call impl_timeout_run')
                self.ui.txtImpl_Log.setPlainText(info.implResult)
                self.ui.txtImpl_Log.moveCursor(QTextCursor.End)
        except Exception as e:
            print('[!] impl_timeout_run() Error : ' + str(e))

    def memory_patch_timeout_run(self):
        try:
            if info.isMemPatch:
                print('call memory_patch_timeout_run')
                self.ui.txtMemoryPatch_Log.setPlainText(info.memoryPatchResult)
                self.ui.txtMemoryPatch_Log.moveCursor(QTextCursor.End)
        except Exception as e:
            print('[!] memory_patch_timeout_run() Error : ' + str(e))



    ###################
    #   ContextMenu   #
    ###################
    def __method_context_menu(self, position):
        menu = QMenu()

        impl_action = menu.addAction('Go to Implementation')
        interceptor_action = menu.addAction('Go to Interceptor')
        tracer_action = menu.addAction('Add to Tracer')

        action = menu.exec_(self.ui.lstMethodResult.mapToGlobal(position))
        sel_class = self.ui.txtMethodClassName.text()
        sel_method = self.ui.lstMethodResult.item(self.ui.lstMethodResult.currentRow(), 0).text()
        if action == interceptor_action:
            self.ui.txtInterceptor_ClassName.setText(sel_class)
            self.ui.txtInterceptor_MethodName.setText(sel_method)
            self.changeInterceptorMethodName()
            self.ui.tabWidget.setCurrentIndex(3)
        elif action == impl_action:
            self.ui.txtImpl_ClassName.setText(sel_class)
            self.ui.txtImpl_MethodName.setText(sel_method)
            self.ui.tabWidget.setCurrentIndex(2)
        elif action == tracer_action:
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            item.setText(sel_method[0] + '[' + sel_class + ' ' + sel_method[2:] + ']')

            self.ui.lstTrace_Filters.setRowCount(self.ui.lstTrace_Filters.rowCount() + 1)
            info.mainUI.ui.lstTrace_Filters.setItem(0, self.ui.lstTrace_Filters.rowCount() - 1, item)

            info.TraceFilterCount += 1

    def __list_context_menu(self, position):
        try:
            menu = QMenu()

            newMenu = menu.addMenu('New')
            newFile = newMenu.addAction('New File')
            newDirectory = newMenu.addAction('New Directory')
            delete = menu.addAction('Delete')
            refresh = menu.addAction('Refresh')

            action = menu.exec_(self.ui.treeScriptList.mapToGlobal(position))

            if action == newFile:
                reply = QInputDialog.getText(self, 'New File', 'Input New FileName', QLineEdit.Normal, '')
                if reply[1]:
                    if not reply[0].endswith('.js'):
                        QMessageBox.warning(self, 'Warning', 'Only JavaScript File')
                        return
                    selectItem = self.ui.treeScriptList.currentItem()
                    path = selectPath(selectItem, reply[0])

                    if os.path.exists(path):
                        reply = QMessageBox.question(self, 'Question',
                                                     'File already exists. Do you want to overwrite it?',
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if reply == QMessageBox.No:
                            return

                    f = open(path, 'w')
                    f.close()
                    self.ui.treeScriptList.clear()
                    createFileSystem(default_File_path + 'User_script\\', self.ui.treeScriptList)
            elif action == newDirectory:
                reply = QInputDialog.getText(self, 'New Directory', 'Input New DirectoryName', QLineEdit.Normal, '')
                if reply[1]:
                    selectItem = self.ui.treeScriptList.currentItem()
                    path = selectPath(selectItem, reply[0])
                    if os.path.exists(path):
                        QMessageBox.information(self, 'Information', 'Directory already exists!!')
                        return

                    os.makedirs(os.path.join(path))
                    self.ui.treeScriptList.clear()
                    createFileSystem(default_File_path + 'User_script\\', self.ui.treeScriptList)
            elif action == delete:
                selectItems = self.ui.treeScriptList.selectedItems()
                for selectItem in selectItems:
                    path = getAbsPath(selectItem, 0)
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            reply = QMessageBox.information(self, 'Question', 'File:' + str(selectItem.text(0)) + '\nReally delete this file?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if reply == QMessageBox.No:
                                return
                            else:
                                os.remove(path)
                        elif os.path.isdir(path):
                            reply = QMessageBox.information(self, 'Question', 'Really delete this directory?\n(포함된 모든 파일이 삭제됩니다)', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if reply == QMessageBox.No:
                                return
                            else:
                                import shutil
                                shutil.rmtree(path)
                self.ui.treeScriptList.clear()
                createFileSystem(default_File_path + 'User_script\\', self.ui.treeScriptList)
            elif action == refresh:
                self.ui.treeScriptList.clear()
                createFileSystem(default_File_path + 'User_script\\', self.ui.treeScriptList)
                self.ui.txtScriptEdit.setPlainText('')
                self.ui.txtScriptEdit.setEnabled(False)

        except Exception as e:
            print(e)

    def __memory_context_menu(self, position):
        try:
            menu = QMenu()

            setStartAddress = menu.addAction('Set Start Address')
            setEndAddress = menu.addAction('Set End Address')

            action = menu.exec_(self.ui.lstMemoryScan_Result.mapToGlobal(position))
            if self.ui.lstMemoryScan_Result.item(self.ui.lstMemoryScan_Result.currentRow(), 0) == None:
                return
            if self.ui.lstMemoryScan_Result.currentColumn() == 17:
                return

            sel_address = int('0x' + self.ui.lstMemoryScan_Result.item(self.ui.lstMemoryScan_Result.currentRow(), 0).text(), 16)
            sel_address += int(self.ui.lstMemoryScan_Result.currentColumn()) - 1

            if action == setStartAddress:
                self.ui.txtMemoryDump_start.setText(str(hex(sel_address)))
                self.ui.txtMemoryPatch_start.setText(str(hex(sel_address)))
            elif action == setEndAddress:
                startAddress = self.ui.txtMemoryDump_start.text()
                if startAddress == '':
                    QMessageBox.warning(info.mainUI, 'Failed', 'Set Start Address First!!')
                    return

                len = sel_address - int(startAddress, 16) + 1
                if len <= 0:
                    QMessageBox.warning(info.mainUI, 'Failed', 'Set Address Bigger Then Start Address')
                    return
                self.ui.txtMemoryDump_end.setText(str(hex(sel_address)))
                self.ui.txtMemoryDump_len.setText(str(len))
                self.ui.txtMemoryPatch_end.setText(str(hex(sel_address)))
                self.ui.txtMemoryPatch_len.setText(str(len))

        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    x = Form()
    info.mainUI = x
    sys.exit(app.exec_())