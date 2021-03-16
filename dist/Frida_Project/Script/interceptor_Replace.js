
		var className{{5}} = '{{0}}';
		var methodName{{5}} = '{{1}}';

		var method{{5}} = eval('ObjC.classes["' + className{{5}} + '"]["' + methodName{{5}} + '"]');
		var sendStr{{5}};
		Interceptor.attach(method{{5}}.implementation, {
			onEnter: function(args) {
				var argNum = {{2}};
				var args_replace = {{3}};
				sendStr{{5}} = 'Call ' + className{{5}} + '["' + methodName{{5}} + '"](';
				
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
							sendStr{{5}} += argTmp + '=>"' + args_replace[i - 2] + '"';
						}else {
							argTmp_replace = ptr(args_replace[i - 2]);
							sendStr{{5}} += argTmp + '=>' + args_replace[i - 2];
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
					var type = eval('ObjC.classes.' + className{{5}} + '["' + methodName{{5}} + '"].returnType');
					if(type == 'bool' || type == 'int')
						retval.replace(ptr({{4}}));
					else if(type == 'void') 
						sendStr{{5}} += '';
					else {
						// retval.replace(ObjC.selector('{{4}}'))
						// retval.replace('{{4}}');	

						var newRet = ObjC.classes.NSString.stringWithString_('{{4}}');
						retval.replace(ptr(newRet));
					}
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
