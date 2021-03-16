class Information:
    def __init__(self):
        self.mainUI = None

        # Server Info
        self.ipAddress = 'http://127.0.0.1:8000'

        # Device
        self.session = None
        self.device_manager = None
        self.device_dict = {}
        self.device = None
        self.process_name = ''
        self.package_name = ''
        self.script_to_load = ''
        self.script = None
        self.gating_option = False

        # Enumerator
        self.classList = []
        self.currentMethodList = []
        self.currentFilePath = ''

        # Script Loader
        self.i = 0
        self.isPlay = False
        self.playResult = ''

        # Function Implement
        self.isImpl = False
        self.implCount = 0
        self.implTemp = {}
        self.implCurrent = []
        self.implScript = ''
        self.implResult = ''

        # Interceptor
        self.isOffset = False

        self.isIntercept = False
        self.interceptType = 'Log'
        self.interceptCount = 0
        self.interceptCurrent = []
        self.interceptScript = ''
        self.interceptResult = ''

        # Debugging
        self.isDebug = False
        self.debugCount = 0
        self.debugScript = ''

        # Memory Scan & Dump
        self.memoryAddress = {}
        self.memoryResult = []
        self.memoryCount = 0
        self.memoryMapsCount = 0

        self.memoryPatchResult = ''
        self.isMemPatch = False

        # API Tracer
        self.isTrace = False
        self.TraceFilterCount = 0
        self.traceScript = ''
        self.traceResult = []
        self.traceSearchResult = []
        self.traceCount = 0

info = Information()
