function searchPattern(target, pattern) {
	Memory.scan(ptr(target[0]), target[1] * 1, pattern, {
		onMatch: function(address, size) {
			send(hexdump(address.sub({{1}}), {
				offset: 0x00,
				length: {{2}}
			}));
		},
		onComplete: function() {
			return;
		}
	});
}

var pattern = "{{0}}";
setTimeout(function() {
	if(ObjC.available) {
		var searchList = {{3}};
		for(var i=0; i<searchList.length; ++i) {
			searchPattern(searchList[i], pattern);
		}
	}
}, 0);