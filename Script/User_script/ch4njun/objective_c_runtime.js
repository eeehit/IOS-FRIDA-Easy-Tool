function getclassMethod(className) {
	var class_copyMethodList = new NativeFunction(Module.findExportByName(null, 'class_copyMethodList'), 'pointer', ['pointer', 'pointer']);
	var method_getName = new NativeFunction(Module.findExportByName(null, 'method_getName'), 'pointer', ['pointer']);
	var method_getImplementation = new NativeFunction(Module.findExportByName(null, 'method_getImplementation'), 'pointer', ['pointer']):

	var pcount = Memory.alloc(4);
	Memory.write(pcount, 0);

	var methodptrarr = class_copyMethodList(className, pcount);
	var count = Memory.readU32(pcount);

	var result = new Array();
	for(var i = 0; i < count; ++i) {
		var method = Memory.readPointer(methodptrarr.add(Process.pointerSize * i);
		var name = Memory.readUtf8String(method_getName(method));
		var impl = method_getImplementation(method);
		result.add('name : ' + name + ', impl : ' +impl);
	}
}