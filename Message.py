from Information import *
import Utils
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def onMessage(message, data):
    try:
        tmpInfo = ''
        if message.get('type') == 'send':
            if message.get('payload') != None:
                tmpInfo = str(message.get('payload'))
            else:
                tmpInfo = 'No message payload..'

        if 'clazzclazz' in tmpInfo:
            tmpInfo = tmpInfo.replace('clazzclazz', '').replace('undefined', '')

            classList = tmpInfo.split('\n')
            info.mainUI.ui.lstClassResult.setRowCount(len(classList) - 1)

            info.mainUI.ui.lstClassResult.clear()
            info.mainUI.ui.lstClassResult.setHorizontalHeaderLabels([''.join(['Name (', str(len(classList) - 1), ')'])])
            for i in range(0, len(classList) - 1):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setText(classList[i])
                info.classList.append(classList[i])
                info.mainUI.ui.lstClassResult.setItem(0, i, item)
            info.mainUI.ui.update()

        if 'mm33tthh00dd' in tmpInfo:
            tmpInfo = tmpInfo.replace('mm33tthh00dd', '').replace('undefined', '')

            methodList = tmpInfo.split('\n')
            info.mainUI.ui.lstMethodResult.setRowCount(len(methodList) - 1)

            info.mainUI.ui.lstMethodResult.clear()
            info.mainUI.ui.lstMethodResult.setHorizontalHeaderLabels([''.join(['Name (', str(len(methodList) - 1), ')'])])
            for i in range(0, len(methodList) - 1):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setText(methodList[i])
                info.currentMethodList.append(methodList[i])
                info.mainUI.ui.lstMethodResult.setItem(0, i, item)
            info.mainUI.ui.update()

        if 'll00aaddll00aadd' in tmpInfo:
            tmpInfo = tmpInfo.replace('ll00aaddll00aadd', '').replace('undefined', '')
            info.playResult += tmpInfo + '\n'

        if 'mm22mmsscc44nn' in tmpInfo:
            tmpInfo = tmpInfo.replace('mm22mmsscc44nn', '').replace('undefined', '')

            info.memoryResult.append(tmpInfo)
            scope = int(info.mainUI.numMemoryScan_scope.text())
            info.mainUI.ui.lstMemoryScan_Result.setRowCount((info.memoryCount + 1) * (scope * 2 + 1 + 1))
            tmpInfo_split = tmpInfo.split()[17:]

            addr_tmp = tmpInfo_split[0][:6]
            x = -1
            y = 0

            for i in range(len(tmpInfo_split)):
                if tmpInfo_split[i].startswith(addr_tmp):
                    x += 1
                    y = 0
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)

                if y > 17:
                    item.setText(info.mainUI.ui.lstMemoryScan_Result.item((info.memoryCount * (scope * 2 + 1 + 1)) + x, 17).text() + ' ' + tmpInfo_split[i])
                    info.mainUI.ui.lstMemoryScan_Result.setItem((info.memoryCount * (scope * 2 + 1 + 1)) + x, 17, item)
                else:
                    item.setText(tmpInfo_split[i])
                    info.mainUI.ui.lstMemoryScan_Result.setItem((info.memoryCount * (scope * 2 + 1 + 1)) + x, y, item)
                y += 1
            info.mainUI.ui.update()
            info.memoryCount += 1

        if 'iinntt22rrcc22pptt' in tmpInfo:
            tmpInfo = tmpInfo.replace('iinntt22rrcc22pptt', '').replace('undefined', '')
            info.interceptResult += tmpInfo + '\n'

        if 'ttrr44cc22' in tmpInfo:
            if info.isTrace:
                tmpInfo = tmpInfo.replace('ttrr44cc22', '').replace('undefined', '')
                info.traceResult.append(str(info.traceCount) + ': ' + tmpInfo)
                if info.mainUI.ui.txtTrace_Search.text() in tmpInfo:
                    info.traceSearchResult.append(str(info.traceCount) + ': ' + tmpInfo)
                info.traceCount += 1

        if 'iimmppll22mm22nntt44ttii00nn' in tmpInfo:
            tmpInfo = tmpInfo.replace('iimmppll22mm22nntt44ttii00nn', '').replace('undefined', '')
            info.implResult += tmpInfo + '\n'

        if 'dd22bbuu99' in tmpInfo:
            tmpInfo = tmpInfo.replace('dd22bbuu99', '').replace('undefined', '')
            register_tmp = tmpInfo.split()
            info.mainUI.ui.txtDebug_CurrentAddress.setText(register_tmp[0])
            info.mainUI.ui.txtDebug_x0.setText(register_tmp[1])
            info.mainUI.ui.txtDebug_x1.setText(register_tmp[2])
            info.mainUI.ui.txtDebug_x2.setText(register_tmp[3])
            info.mainUI.ui.txtDebug_x3.setText(register_tmp[4])
            info.mainUI.ui.txtDebug_x4.setText(register_tmp[5])
            info.mainUI.ui.txtDebug_x5.setText(register_tmp[6])
            info.mainUI.ui.txtDebug_x6.setText(register_tmp[7])
            info.mainUI.ui.txtDebug_x7.setText(register_tmp[8])
            info.mainUI.ui.txtDebug_x8.setText(register_tmp[9])
            info.mainUI.ui.txtDebug_x9.setText(register_tmp[10])
            info.mainUI.ui.txtDebug_x10.setText(register_tmp[11])
            info.mainUI.ui.txtDebug_x11.setText(register_tmp[12])
            info.mainUI.ui.txtDebug_x12.setText(register_tmp[13])
            info.mainUI.ui.txtDebug_x13.setText(register_tmp[14])
            info.mainUI.ui.txtDebug_x14.setText(register_tmp[15])
            info.mainUI.ui.txtDebug_x15.setText(register_tmp[16])
            info.mainUI.ui.txtDebug_x16.setText(register_tmp[17])
            info.mainUI.ui.txtDebug_x17.setText(register_tmp[18])
            info.mainUI.ui.txtDebug_x18.setText(register_tmp[19])
            info.mainUI.ui.txtDebug_x19.setText(register_tmp[20])
            info.mainUI.ui.txtDebug_x20.setText(register_tmp[21])
            info.mainUI.ui.txtDebug_x21.setText(register_tmp[22])
            info.mainUI.ui.txtDebug_x22.setText(register_tmp[23])
            info.mainUI.ui.txtDebug_x23.setText(register_tmp[24])
            info.mainUI.ui.txtDebug_x24.setText(register_tmp[25])
            info.mainUI.ui.txtDebug_x25.setText(register_tmp[26])
            info.mainUI.ui.txtDebug_x26.setText(register_tmp[27])
            info.mainUI.ui.txtDebug_x27.setText(register_tmp[28])
            info.mainUI.ui.txtDebug_x28.setText(register_tmp[29])
            info.mainUI.ui.txtDebug_x29.setText(register_tmp[30])
            info.mainUI.ui.txtDebug_BaseAddress.setText(register_tmp[31])

        if 'mm44pp22' in tmpInfo:
            tmpInfo = tmpInfo.replace('mm44pp22', '').replace('undefined', '')
            address_tmp = tmpInfo.split('\n')

            for i in address_tmp[:-1]:
                info.mainUI.lstMemoryScan_Address.setRowCount(info.memoryMapsCount + 1)
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setText(i.split(' ')[0])
                info.mainUI.lstMemoryScan_Address.setItem(info.memoryMapsCount, 0, item)

                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                item.setText(i.split(' ')[1])
                info.mainUI.lstMemoryScan_Address.setItem(info.memoryMapsCount, 1, item)

                info.memoryMapsCount += 1
            Utils.unloadScript()

        if 'rr22pp1144cc2244llll' in tmpInfo:
            tmpInfo = tmpInfo.replace('rr22pp1144cc2244llll', '').replace('undefined', '')
            info.memoryPatchResult += tmpInfo + '\n'

    except Exception as e:
        print('[!] onMessage() Error : ' + str(e))