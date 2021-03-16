		var targetModule{{5}} = Process.enumerateModules()[0].name;
    		var address{{5}} = ptr({{1}});
    		var moduleBase{{5}} = Module.getBaseAddress(targetModule{{5}});
    		var targetAddress{{5}} = moduleBase{{5}}.add(address{{5}}); 
		var sendStr{{5}};

		Interceptor.attach(targetAddress{{5}}, {
			onEnter: function(args) {
				var argNum = {{2}};
				var args_replace = {{3}};
				sendStr{{5}} = 'Call ' + targetAddress{{5}} + '(';
				
				for(var i = 2; i < 2 + argNum; ++i) {
					var argTmp;
					try {
						if(!args[i].toString.equals('0x0')) {
							argTmp = '"' + Memory.readUtf8String(ptr(args[i].toString())) + '"';
						}else {
							argTmp = args[i].toString();
						}
					}catch(e) {
						if(args[i].toString().length > 10) {
							argTmp = '"' + new ObjC.Object(args[i]).toString() + '"';
						}else {
							argTmp = args[i].toString();
						}
					}

					if(args_replace[i - 2] == '') 
						sendStr{{5}} += argTmp;
					else{
						var argTmp_replace;
						if(args[i].toString().length > 10) {
							argTmp_replace = new ObjC.Object(ObjC.classes.NSString.stringWithString_(args_replace[i - 2]));
							sendStr{{5}} += argTmp + '=> "' + args_replace[i - 2] + '"';
						}else {
							argTmp_replace = ptr(args_replace[i - 2]);
							sendStr{{5}} += argTmp + "=>" + args_replace[i - 2];
						}
						
						args[i] = argTmp_replace;	
					}
					sendStr{{5}} += (i < 1 + argNum) ? ', ' : ') ';
				}
				if(argNum == 0)
					sendStr{{5}} += ')';
			},
			onLeave: function(retval) {
				var obj;
				try {
					if(!retval.toString.equals('0x0')) {
						obj = '"' + Memory.readUtf8String(ptr(retval)) + '"';
					}else {
						obj = retval.toString();
					}
				}catch(e) {
					if(retval.toString().length > 10) {
						obj = '"' + new ObjC.Object(retval).toString() + '"';
					}else {
						obj = retval.toString();
					}
				}
				sendStr{{5}} += '=> (' + obj;

				if('{{4}}' != '') {
					var newRet;
					if('{{6}}' == 'string') {
						newRet = ObjC.classes.NSString.stringWithString_('{{4}}');
					}else if('{{6}}' == 'int' || '{{6}}' == 'bool') {
						newRet = ptr({{4}});
					}
					retval.replace(ptr(newRet));
				}
				
				var obj2;
				try {
					if(!retval.toString.equals('0x0')) {
						obj2 = '"' + Memory.readUtf8String(ptr(retval)) + '"';
					}else {
						obj2 = retval.toString();
					}
				}catch(e) {
					if(retval.toString().length > 10) {
						obj2 = '"' + new ObjC.Object(retval).toString() + '"';
					}else {
						obj2 = retval.toString();
					}
				}
				sendStr{{5}} += ' => ' + obj2 + ')';
				send(sendStr{{5}});

				return retval;
			}
		});
