if(ObjC.available) {
	try {
		var className = "JailbreakDetectionVC";
		var methodName = "- isJailbroken";
 		var hookMathod = eval("ObjC.classes." + className + '["'  + methodName + '"]');
        
		Interceptor.attach(hookMethod.implementation, {
			onEnter: function(args) {
 				var receiver = new ObjC.Object(args[0]);

				console.log("Target class : " + receiver.$className);
				console.log("Target superclass : " + receiver.$superClass.$className);

				var selector = ObjC.selectorAsString(args[1]);
				console.log("typeof selector = " + typeof selector);

				console.log("Hooked the target method : " + selector);
				// Parameter는 args[2] 에 위치한다.
			}
			,onLeave: function(retval) {
				console.log("[>] retval Type : " + typeof retval);
				console.log("[>] retval Value : " + retval);
			}
		});

	}catch(err) {
		console.log("[!] Exception: " + err.message);
	}
}