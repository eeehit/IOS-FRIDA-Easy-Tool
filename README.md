# Readme
## IOS FRIDA Easy Tool?

IOS의 Application을 진단할 때 FRIDA를 사용하게 되는데, 이 과정에서 아래와 같은 불편함을 개선하기 위해 진행한 프로젝트이다.

1. JavaScript 및 Python을 위한 Editor를 별도로 사용해야 하고, FRIDA 명령어를 실행하기 위한 CMD 창을 띄워 사용해야 한다. 이 때 여러 화면을 오가며 사용해야 한다는 번거로움이 있다.
2. FRIDA의 복잡한 명령어를 숙지하고 있어야 하고, Frida-trace와 같은 유용한 툴마다 별도의 명령어를 숙지하고 있어야 하는 어려움이 있다.
3. FRIDA에서 사용하는 Script를 작성하는데 지식이 필요하다. 간단하고 반복적인 동작을 하는 Script를 작성하는데 꽤 많은 양의 코드를 작성해야 할 수 있다.
4. 여러 Function(API)에 대해서 동일한 Hooking/Interceptor 등 작업을 수행할 경우, 동일한 Script를 Function에 대한 정보만 변경해 일일히 반복해서 작성해야하는 번거로움이 있다.
5. 자신이 사용했던 Script의 종류가 많아지면서 관리가 어려워지고, 협업을 위해 Script를 공유하려면 별도의 메일, SNS등의 방법을 사용해야 하는 번거로움이 있다.

## Usage
1. 진단에 사용할 iPhone에 Frida-Server를 설치한다.
2. 진단에 사용할 PC에 같은 버전의 Frida와 Frida-tools를 설치한다.
3. iPhone에 넣은 Frida-Server를 Background로 실행한다.
4. iPhone을 USB로 해당 PC에 연결한다.
5. 다운로드 받은 IOS FRIDA Easy Tool.zip을 풀고 exe파일을 실행한다.
6. Device&Package 버튼을 통해 진단에 사용할 iPhone과 Application을 선택한다.
7. 아래 항목별 설명에 따라 필요한 기능을 사용한다.

<br>

> 제공하는 웹 서버는 Script를 백업하거나, 내부에서 협업을 위해 Script를 공유하기 위해 사용할 수 있고, Repository 단위로 Script를 저장한다.

1. Web-server를 실행시킬 PC에 [Docker](https://docs.docker.com/docker-for-windows/install/)를 설치한다.
2. Web-server.zip 파일을 압축해제하고 cmd창을 이용해 해당 폴더로 이동한다.
3. `docker-compose up` 명령어를 실행한다.
4. `127.0.0.1:8000` 혹은 `IP주소:8000` 으로 연결해 Web-server에 접속한다.

<br>

---
## Enumerator
Enumerator에서는 아래 3가지 기능을 제공한다.
1. Application에 포함된 Class의 목록을 읽어온다.
2. 특정 Class에 대해해 포함된 Method 목록을 읽어온다.
3. Script를 생성/수정/삭제할 수 있는 파일 탐색기를 제공한다. 연결된 Web-Server를 통해 Script를 업로드&다운로드할 수 있다.

---
## Script Loader
Script Loader는 특정 Script를 Application에 주입해 그 결과를 로그창을 통해 확인할 수 있다.

---
## Hook Implement
Class&Method 이름을 통해 대상 API를 원하는 내용으로 변조하는 Hooking을 수행할 수 있다.

---
## Interceptor
Interceptor에서는 아래 2가지 기능을 제공한다.
1. Class&Method 이름 혹은 Offset을 통해 대상 API가 호출될 때 Parameter&Call Stack&Return value 를 확인할 수 있다. (Log)
2. Class&Method 이름 혹은 Offset을 통해 대상 API가 호출될 때 Parameter&Return value를 변조할 수 있다. (Replace)

---
## Debugger
Address(Offset)을 입력하고 추가할 경우 Break Point가 설정되고, Application이 진행되면서 해당 Address의 명령어가 호출될 경우 Application이 멈춘다. 이 때 Register 정보를 확인할 수 있고 이를 변조할 수도 있다.

---
## Memory
Memory에서는 아래 5가지 기능을 제공한다.
1. Memory Maps를 통해 현재 프로세스에서 사용중인 메모리영역의 Start Address&Size를 확인할 수 있다.
2. 선택한 메모리 영역에서 String&Hex 값을 탐색할 수 있다.
3. Start&End Address를 통해 메모리 영역을 Dump할 수 있다.
4. Start&End Address를 통해 특정 메모리 영역을 원하는 값(String&Hex)로 Replace할 수 있다.
5. Application에 존재하는 특정 문자열을 원하는 값(Only String)으로 일괄적으로 Replace할 수 있다.

---
## API Trace
Trace할 API목록을 입력하고, Application을 사용하게 되면 해당 API가 호출될 때 Parameter&Call Stack&Return value를 확인할 수 있다. Trace할 API목록은 `*[ClassName* *]` 와 같이 와일드카드를 사용해 작성할 수 있다.