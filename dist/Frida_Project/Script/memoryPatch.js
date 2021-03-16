setTimeout(function() {
	if(ObjC.available) {
		var original_protection = Process.findRangeByAddress(ptr({{0}})).protection;
		Memory.protect(ptr({{0}}), {{1}}, 'rwx');
		Memory.writeByteArray(ptr({{0}}), {{2}});
		Memory.protect(ptr({{0}}), {{1}}, original_protection);
	}
}, 0);