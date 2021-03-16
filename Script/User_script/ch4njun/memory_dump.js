function searchPattern(pattern) {
	var memRanges = Process.enumerateRangesSync({protection: 'r--', coalesce: true});
	var memRange;

	function Next_Range() { // ��͸� ������ ���ؼ� �����Լ�.
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
					length: 0x30 // �ֺ��� �� Byte���� Ȯ������ ����.
				}));
			},
			onComplete: function() {
				Next_Range();  // ����Լ� ȣ��.
			}
		});
	}
	Next_Range();  // ����ȣ��.
}

pattern = "42 6f ?? 62 79";  // Bo?by �� ���� ���ϵ�ī�带 ����Ҽ��� �ִ�.
if(ObjC.available) {
	searchPattern(pattern);
}