setTimeout(function() {
	if(ObjC.available) {
		var moduleName = 'DVIA-v2';
		var address = ptr(0x1959cc);
		var moduleBase = Module.getBaseAddress(moduleName);
		var targetAddress = moduleBase.add(address);

		Interceptor.attach(targetAddress, {
			onEnter: function(args) {
				send('before x8 : ' + this.context.x8);
				send('ch4njun' + this.context.x8);
				
				var result;
				recv(function(string_to_recv) {
					result = string_to_recv.my_data;
				}).wait();
				this.context.x8 = result * 1;
				send('after x8 : ' + this.context.x8);
			},
		});
	}
}, 0);