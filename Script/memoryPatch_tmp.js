setTimeout(function() {
	if(ObjC.available) {
		var original_protection = Process.findRangeByAddress(ptr(0x28227f761)).protection;
		Memory.protect(ptr(0x28227f761), 16, 'rwx');
		Memory.writeByteArray(ptr(0x28227f761), ['0x63', '0x68', '0x34', '0x6e', '0x6a', '0x75', '0x6e', '0x69', '0x69', '0x20', '0x74', '0x74', '0x74', '0x74', '0x20', '0x30']);
		Memory.protect(ptr(0x28227f761), 16, original_protection);
	}
}, 0);