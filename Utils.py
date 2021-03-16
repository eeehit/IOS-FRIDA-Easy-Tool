import frida, sys, os
from Message import *
from PyQt5.QtWidgets import *
from frida import ProcessNotFoundError

default_UI_path = "UI\\"
default_File_path = "Script\\"
default_Output_path = os.path.expanduser('~') + '\\Desktop\\'

def getDevices():
    print("[+] getDevices()")
    try:
        info.device_dict = {}
        info.device_manager = frida.get_device_manager()
        device_list = info.device_manager.enumerate_devices()

        remote_device_list = []

        if len(device_list) != 0:
            for dv in device_list:
                if str(dv.id) != 'local' and str(dv.id) != 'socket':
                    remote_device_list.append(dv)

        for dv in remote_device_list:
            info.device_dict[str(dv.id)] = str(dv)
    except Exception as e:
        info.device = None
        print("[!] getDevices() Error : ", str(e))

def setDevice(dv_id):
    print("[+] setDevice : ", dv_id)
    info.device = info.device_manager.get_device(dv_id)

def loadScript():
    if (info.script_to_load != '') and (info.package_name != '') and (info.device != None):
        if not info.isDebug:
            unloadScript()
        else:
            killProcess()
        print("[+] loadScript()")

        try:
            pending = False
            try:
                pid = info.device.get_process(info.process_name).pid
                info.session = info.device.attach(info.process_name)
            except ProcessNotFoundError as e:
                # gating_option
                # 여기서 gating_option이 False면 pending이 True가 된다.
                if info.gating_option:
                    info.device.enable_spawn.gating()
                    #info.device.on('spawn-added', on_spawned)
                    return
                else:
                    pid = info.device.spawn([info.package_name])
                    info.session = info.device.attach(pid)
                    pending = True
            info.script = info.session.create_script(info.script_to_load)
            info.script.on('message', onMessage)
            info.script.load()
            print(info.script_to_load)
            if pending:
                info.device.resume(pid)
        except Exception as e1:
            print("[!] loadScript() Error : " + str(e1))
            QMessageBox.warning(info.mainUI, 'Failed', '[!] loadScript() Error\n' + str(e1))

def unloadScript():
    print('[+] unloadScript()')
    try:
        if info.session:
            info.script.unload()  # : 자꾸 느려지는 문제 발생... 대체하긴했는데 뭔가 불안한 부분이다.
            # info.device.kill(info.process_name) # : 되긴하는데 매번 unload할때마다 Proccess를 꺼버린다.
            # info.session.detach()
        else:
            print("[-] No script exists!")
    except Exception as e:
        print("[!] unloadScript() Error : " + str(e))

def killProcess():
    print('[+] killProcess()')
    try:
        if info.session:
            info.device.kill(info.process_name)
            info.isDebug = False
        else:
            print('[-] No script exists!')
    except Exception as e:
        print('[!] killProcess() Error : ' + str(e))

def renderScript(filePath, *args):
    print("[+] renderScript(", filePath, ")", args, sep='')
    try:
        f = open(filePath, "r")
        data = f.read()
        f.close()

        for index in range(len(args)):
            data = data.replace(''.join(['{{', str(index), '}}']), args[index])

        f = open(''.join([filePath[:-3], "_tmp.js"]), "w")
        f.write(data)
        f.flush()
        f.close()
    except Exception as e:
        print("[!] renderScript() Error : " + str(e))

def scriptSave(filePath, data):
    print('[+] scriptSave(', filePath, ', ', data, ')', sep='')
    try:
        f = open(filePath, "w")
        f.write(data)
        f.flush()
        f.close()
        QMessageBox.information(info.mainUI, 'Succeed', 'Script Save Success!')
    except Exception as e:
        QMessageBox.warning(info.mainUI, 'Faild', 'Script Save Faild!')

def getAbsPath(file, index):
    try:
        tmpItem = file
        filePath = default_File_path + "User_Script\\"

        lst = []
        while tmpItem.parent() != None:
            lst.append('\\')
            lst.append(tmpItem.parent().text(0))
            tmpItem = tmpItem.parent()
        lst.reverse()
        filePath += ''.join(lst)
        filePath += file.text(index)

        return filePath
    except Exception as e:
        print('[!] getAbsPath() Error : ' + str(e))

def getAllFile(path):
    try:
        fileList = []
        if os.path.isfile(path):
            fileList.append(path)
        elif os.path.isdir(path):
            fileList.extend(getSubDirList(path + '\\'))
        return fileList
    except Exception as e:
        print('[!] getAllFile() Error : ' + str(e))

def getSubDirList(dir):
    lst = []
    fileList = os.listdir(dir)
    for file in fileList:
        target = dir + file
        if os.path.isfile(target):
            lst.append(target)
        elif os.path.isdir(target):
            lst.extend(getSubDirList(target + '\\'))
    return lst

def createFileSystem(rootPath, parent):
    print('[+] createFileSystem()')
    try:
        for name in os.listdir(rootPath):
            if name.endswith('.js'):
                item = QTreeWidgetItem(parent)
                item.setText(0, name)
            elif os.path.isdir(rootPath + name):
                item = QTreeWidgetItem(parent)
                item.setText(0, name)
                createFileSystem(rootPath + name + '\\', item)
    except Exception as e:
        print('[!] createFileSystem() Error : ' + str(e))

def saveScript(data, type):
    try:
        reply = QInputDialog.getText(info.mainUI, 'New File', 'Input New FileName', QLineEdit.Normal, '')
        if reply[1]:
            if not reply[0].endswith('.js'):
                QMessageBox.warning(info.mainUI, 'Warning', 'Only JavaScript File')
                return
            selectItem = info.mainUI.ui.treeScriptList.currentItem()
            if selectItem == None:
                return

            if type == 0:
                filePath = default_File_path
            elif type == 1:
                filePath = getAbsPath(selectItem, 0)

            if os.path.isfile(filePath):
                filePath = '\\'.join(filePath.split('\\')[:-1])

            if filePath == default_File_path:
                filePath += 'User_script\\'
            filePath += '\\' + reply[0]

            if os.path.exists(filePath):
                reply = QMessageBox.question(info.mainUI, 'Question', 'File already exists. Do you want to overwrite it?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    return
            scriptSave(filePath, data)
    except Exception as e:
        print('[!] saveScript() Error : ' + str(e))
        QMessageBox.warning(info.mainUI, 'Warning', str(e))

def memoryScanTypeCheck(input, type):
    if type == 'Hex':
        try:
            for i in range(0, len(input), 3):
                if len(input[i:i + 3].strip()) == 3:
                    return False

                if input[i:i + 3].strip() == '??':
                    continue
                chr(int(input[i:i + 3].strip(), 16))
        except Exception as e:
            return False
        return True

def str2hex(input):
    try:
        tmp = ''
        for i in range(len(input)):
            tmp += str(hex(ord(input[i])))[2:] + ' '
        return tmp.strip()
    except Exception as e:
        print('[!] str2hex() Error : ' + str(e))

def numOfEnable(num):
    try:
        for i in range(num):
            eval('info.mainUI.ui.txtInterceptor_arg' + str(i) + '.setEnabled(True)')

        for i in range(num, 8):
            eval('info.mainUI.ui.txtInterceptor_arg' + str(i) + '.clear()')
            eval('info.mainUI.ui.txtInterceptor_arg' + str(i) + '.setEnabled(False)')
    except Exception as e:
        print('[!] numOfEnable() Error : ' + str(e))

def selectPath(selectItem, fileName):
    if selectItem == None:
        path = default_File_path + 'User_script'
    else:
        path = getAbsPath(selectItem, 0)

    if os.path.isfile(path):
        path = '\\'.join(path.split('\\')[:-1])
    path += '\\' + fileName
    return path

def createInterceptScript():
    print('[+] createInterceptScript()')
    try:
        f = open(default_File_path + 'common_head.js', 'r')
        data = f.read()
        f.close()

        for i in range(info.interceptCount):
            tmpDict = info.interceptCurrent[i]

            if tmpDict['className'] == 'NULL':
                if tmpDict['type'] == 'Log':
                    renderScript(default_File_path + 'interceptor_Offset_Log.js', info.process_name, tmpDict['methodName'],
                                 tmpDict['argc'], str(i), str(info.mainUI.ui.checkInterceptor_callstack.isChecked()))
                    f = open(default_File_path + 'interceptor_Offset_Log_tmp.js', 'r')
                    data += f.read()
                    f.close()
                    os.remove(default_File_path + 'interceptor_Offset_Log_tmp.js')
                elif tmpDict['type'] == 'Replace':
                    arg_lst = []
                    for j in range(int(tmpDict['argc'])):
                        arg_lst.append(tmpDict[j])
                    renderScript(default_File_path + 'interceptor_Offset_Replace.js', info.process_name,
                                 tmpDict['methodName'], tmpDict['argc'], str(arg_lst), tmpDict['retval'], str(i), str(info.mainUI.ui.comboInterceptor_returnType.currentText()))
                    f = open(default_File_path + 'interceptor_Offset_Replace_tmp.js', 'r')
                    data += f.read()
                    f.close()
                    os.remove(default_File_path + 'interceptor_Offset_Replace_tmp.js')
            else:
                if tmpDict['type'] == 'Log':
                    renderScript(default_File_path + 'interceptor_Log.js', tmpDict['className'], tmpDict['methodName'],
                                 tmpDict['argc'], str(i), str(info.mainUI.ui.checkInterceptor_callstack.isChecked()))
                    f = open(default_File_path + 'interceptor_Log_tmp.js', 'r')
                    data += f.read()
                    f.close()
                    os.remove(default_File_path + 'interceptor_Log_tmp.js')
                elif tmpDict['type'] == 'Replace':
                    arg_lst = []
                    for j in range(int(tmpDict['argc'])):
                        arg_lst.append(tmpDict[j])
                    renderScript(default_File_path + 'interceptor_Replace.js', tmpDict['className'], tmpDict['methodName'], tmpDict['argc'], str(arg_lst), tmpDict['retval'], str(i))
                    f = open(default_File_path + 'interceptor_Replace_tmp.js', 'r')
                    data += f.read()
                    f.close()
                    os.remove(default_File_path + 'interceptor_Replace_tmp.js')
        f = open(default_File_path + 'common_tail.js', 'r')
        data += f.read()
        f.close()

        info.interceptScript = data
    except Exception as e:
        print('[-] createInterceptScript() Error : ' + str(e))

def createTraceScript():
    print('[+] createTraceScript()')
    try:
        arg_lst = []
        for i in range(info.TraceFilterCount):
            arg_lst.append(info.mainUI.ui.lstTrace_Filters.item(i, 0).text())

        renderScript(default_File_path + 'trace.js', str(arg_lst), str(info.mainUI.ui.checkTrace_Callstack.isChecked()))
        f = open(default_File_path + 'trace_tmp.js', 'r')
        data = f.read()
        f.close()
        os.remove(default_File_path + 'trace_tmp.js')
        info.traceScript = data
    except Exception as e:
        print('[-] createTraceScript() Error : ' + str(e))

def createImplScript():
    print('[+] createImplScript()')
    try:
        f = open(default_File_path + 'common_head.js', 'r')
        data = f.read()
        f.close()

        for i in range(len(info.implCurrent)):
            data += info.implCurrent[i]['script'] + '\n'

        f = open(default_File_path + 'common_tail.js', 'r')
        data += f.read()
        f.close()

        info.implScript = data
    except Exception as e:
        print('[-] createImplScript() Error : ' + str(e))

def extractContent(data):
    print('[+] extractContent(', data, ')', sep='')
    try:
        reply = QInputDialog.getText(info.mainUI, 'Class List Extract', 'File Name', QLineEdit.Normal, '')
        if reply[1]:
            flag = False
            for i in '\\/*:?"<>|':
                if i in reply[0]:
                    flag = True
                    break
            if flag:
                QMessageBox.warning(info.mainUI, 'Warning', 'Invalid File Name\n(File Name shouldn\'t contain \\/*:?"<>|)')
                return

            if os.path.exists(default_Output_path + reply[0] + '.txt'):
                reply1 = QMessageBox.question(info.mainUI, 'Question', 'File already exists. Do you want to overwrite it?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply1 == QMessageBox.No:
                    return
                elif reply1 == QMessageBox.Yes:
                    os.remove(default_Output_path + reply[0] + '.txt')
            f = open(default_Output_path + reply[0] + '.txt', 'w')
            f.write(data)
            f.flush()
            f.close()
    except Exception as e:
        print('[-] extractContent() Error : ' + str(e))

def createDebugScript():
    print('[+] createDebugScript()')
    try:
        f = open(default_File_path + 'common_head.js', 'r')
        data = f.read()
        f.close()

        for i in range(info.mainUI.ui.lstDebug_BPAddress.rowCount()):
            renderScript(default_File_path + 'debug_breakpoint_address.js', info.process_name, info.mainUI.ui.lstDebug_BPAddress.item(i, 0).text(), str(i))
            f = open(default_File_path + 'debug_breakpoint_address_tmp.js', 'r')
            data += f.read()
            f.close()
            os.remove(default_File_path + 'debug_breakpoint_address_tmp.js')

        f = open(default_File_path + 'common_tail.js', 'r')
        data += f.read()
        f.close()

        info.debugScript = data
    except Exception as e:
        print('[-] createDebugScript() Error : ' + str(e))