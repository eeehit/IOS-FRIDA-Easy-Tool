rpc.exports = {
	readMemory: function(address, size) {
		return Memory.readByteArray(ptr(address), size);
	}
};