setTimeout(function() {
	if(ObjC.available) {
		var sendStr = ''
		for(var clazzName in ObjC.classes) 
			if(ObjC.classes.hasOwnProperty(clazzName)) 
				sendStr += String(clazzName) + '\n';
		send(sendStr);
	}
}, 0);