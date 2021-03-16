function memoryMaps() {
	var memRanges = Process.enumerateRangesSync({protection: 'r--', coalesce:true});
	var memRange;
	var sendMsg = ''

	function Next_Range() {
		try {
			memRange = memRanges.pop();
			sendMsg += memRange.base + " " + memRange.size + "\n";
			if(!memRange) {
				send(sendMsg);
				return;
			}
		}catch(e0) {
			send(sendMsg);
			return;
		}
		Next_Range();
	}
	Next_Range();
}

setTimeout(function() {
	if(ObjC.available) {
		memoryMaps();
	}
}, 0);