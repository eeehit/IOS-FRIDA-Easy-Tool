setTimeout(function() {
	Java.perform(function() {
		var a = Java.use("sg.vantagepoint.a.a");
		a.a.overload("[B", "[B").implementation = function(arg1, arg2) {
			var String = Java.use("java.lang.String");
			var retval = String.$new(this.a(arg1, arg2));
			
			console.log("[+] retval : " + retval);
			return this.a(arg1, arg2);
		}
	});
}, 0);