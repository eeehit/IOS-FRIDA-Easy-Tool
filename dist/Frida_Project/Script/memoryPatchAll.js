function searchPattern(target, pattern) {
	Memory.scan(ptr(target[0]), target[1] * 1, pattern, {
		onMatch: function(address, size) {
			send('Replace Success : ' + address + ' ' + size);
			var original_protection = Process.findRangeByAddress(ptr(address)).protection;
			Memory.protect(ptr(address), size, 'rwx');
			Memory.writeByteArray(ptr(address), {{2}});
			Memory.protect(ptr(address), size, original_protection);
		},
		onComplete: function() {
			return;
		}
	});
}

var pattern = "{{0}}";
setTimeout(function() {
	if(ObjC.available) {
		send('Replace All Start!!!');
		var searchList = {{1}};
		for(var i=0; i<searchList.length; ++i) {
			searchPattern(searchList[i], pattern);
		}
	}
}, 0);