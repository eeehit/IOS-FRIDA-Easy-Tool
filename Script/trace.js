// generic trace
function trace(pattern)
{
    var type = (pattern.indexOf(" ") === -1) ? "module" : "objc";
    var res = new ApiResolver(type);
    var matches = res.enumerateMatchesSync(pattern);
    var targets = uniqBy(matches, JSON.stringify);
	
    targets.forEach(function(target) {
      if (type === "objc")
          traceObjC(target.address, target.name);
      else if (type === "module")
          traceModule(target.address, target.name);
  });
}

// remove duplicates from array
function uniqBy(array, key) 
{
    var seen = {};
    return array.filter(function(item) {
        var k = key(item);
        return seen.hasOwnProperty(k) ? false : (seen[k] = true);
    });
}

// trace ObjC methods
function traceObjC(impl, name)
{
    send('Tracing ' + name);

    Interceptor.attach(impl, {
        onEnter: function(args) {
            send('[+] entered ' + name);
            // print caller
            send('    Caller: ' + DebugSymbol.fromAddress(this.returnAddress));
			
			var name_tmp = name.toString();
			var argc = name_tmp.split(':').length - 1;
			for(var i = 2; i < 2 + argc; ++i) {
				try {
					send('    args[' + i + ']: ' + args[i] + ', ' + Memory.readUtf8String(ptr(args[i].toString())));
				}catch(e) {
					if(args[i].toString().length > 10) {
						send('    args[' + i + ']: ' + args[i] + ', ' + ObjC.Object(args[i]).toString());
					}else {
						send('    args[' + i + ']: ' + args[i] + ', ' + args[i].toString());
					}
				}
				
			}
			
			if('{{1}}' == 'True') {
				send('    [ Backtrace ]\n        ' + Thread.backtrace(this.context, Backtracer.ACCURATE)
                   .map(DebugSymbol.fromAddress).join("\n        "));
			}
        },
        onLeave: function(retval) {
            send('    retval: ' + retval);
            send('[-] exiting ' + name);
        }
    });
}

// trace Module functions
function traceModule(impl, name)
{
    send('Tracing ' + name);

    Interceptor.attach(impl, {
        onEnter: function(args) {
            send("*** entered " + name);
            // print backtrace
            send('    [ Backtrace ]\n        ' + Thread.backtrace(this.context, Backtracer.ACCURATE)
                   .map(DebugSymbol.fromAddress).join("\n        "));
        },
        onLeave: function(retval) {
            send('    retval: ' + retval);
            send('*** exiting ' + name);
        }
    });
}

setTimeout(function() {
	// usage examples.
	if (ObjC.available) {
		var args = {{0}};
		for(var i = 0; i < args.length; ++i) 
			trace(args[i]);
		
	} else {
		send("error: Objective-C Runtime is not available!");
	}
}, 0);