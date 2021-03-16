setTimeout(function() {
	if(ObjC.available) {
		var _window = ObjC.classes.UIWindow.keyWindow();
		var rootControl = _window.rootViewController();
		var control = rootControl['- _printHierarchy']().toString();

		console.log(control);
	}
}, 0);