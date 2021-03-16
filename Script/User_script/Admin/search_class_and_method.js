if(ObjC.available) {
	try {
		for(var class in ObjC.classes) {
			if(ObjC.classes.hasOwnProperty(class)) 
				console.log("[-] " + class);
		}
	}catch(err) {
		console.log("[!] Exception: " + err.message);
	}
}
console.log("[*] Completed: Find All Methods of a Specific Class");
if(ObjC.available) { 
	try { 
		var className = "JailbreakDetectionVC";
		var methods = eval('ObjC.classes.' + className + '.$methods'); 
                
		for(var i = 0; i < methods.length; ++i) { 
			try{ console.log("[-] " + methods[i]); }
			catch(err) { console.log("[!] Exception1: " + err.message); } 
		} 
	}catch(err) { 
		console.log("[!] Exception: " + err.message); 
	} 
} 
console.log("[*] Completed: Find All Methods of a Specific Class");