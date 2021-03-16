		var targetModule{{3}} = Process.enumerateModules()[0].name;
    		var address{{3}} = ptr({{1}});
    		var moduleBase{{3}} = Module.getBaseAddress(targetModule{{3}});
    		var targetAddress{{3}} = moduleBase{{3}}.add(address{{3}}); 
		var sendStr{{3}};
		var sendTmp{{3}};

		Interceptor.attach(targetAddress{{3}}, {
			onEnter: function(args) {
				var argNum = {{2}};
				sendStr{{3}} = 'Call ' + targetAddress{{3}} + '(';
				for(var i = 2; i < 2 + argNum; ++i) {
					var obj;
					try {
						if(!args[i].toString.equals('0x0')) {
							obj = '"' + Memory.readUtf8String(ptr(args[i].toString())) + '"';
						}else {
							obj = args[i].toString();
						}
					}catch(e) {
						if(args[i].toString().length > 10) {
							obj = new ObjC.Object(args[i]).toString();
						}else {
							obj = args[i].toString();
						}
					}
					sendStr{{3}} += obj;
					if(i < 1 + argNum)
						sendStr{{3}} += ', ';
				}
				
				sendStr{{3}} += ') ';
				if('{{4}}' == 'True')
					sendTmp{{3}} = '\n    [ Backtrace ]\n        ' + Thread.backtrace(this.context, Backtracer.ACCURATE)
                   .map(DebugSymbol.fromAddress).join("\n        ");
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
				sendStr{{3}} += '=> ' + obj;
				if('{{4}}' == 'True')
					sendStr{{3}} += sendTmp{{3}};
				send(sendStr{{3}});
			}
		});
