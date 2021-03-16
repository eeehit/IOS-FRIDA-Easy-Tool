setTimeout(function() {
	if(ObjC.available) {
		var sendStr = '';
		var className = '0x123';
		var methods = eval('ObjC.classes["' + className + '"].$ownMethods');
		for(var i = 0; i < methods.length; ++i)
			sendStr += methods[i] + '\n';		
		send(sendStr);
	}
}, 0);