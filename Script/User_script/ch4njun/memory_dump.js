function searchPattern(pattern) {
	var memRanges = Process.enumerateRangesSync({protection: 'r--', coalesce: true});
	var memRange;

	function Next_Range() { // 재귀를 돌리기 위해서 내부함수.
		memRange = memRanges.pop();
		if(!memRange) {
			console.log("Memory Scan Done!!");
			return;
		}

		Memory.scan(memRange.base, memRange.size, pattern, {
			onMatch: function(address, size) {
				console.log("");
				console.log("Memory.scan() found match at " + address + " with size " + size);
				console.log(hexdump(address.sub(0x10), {
					offset: 0x00,
					length: 0x30 // 주변에 몇 Byte까지 확인할지 결정.
				}));
			},
			onComplete: function() {
				Next_Range();  // 재귀함수 호출.
			}
		});
	}
	Next_Range();  // 최초호출.
}

pattern = "42 6f ?? 62 79";  // Bo?by 와 같이 와일드카드를 사용할수도 있다.
if(ObjC.available) {
	searchPattern(pattern);
}