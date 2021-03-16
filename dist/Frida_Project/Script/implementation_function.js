var className{{0}} = '{{1}}';
var methodName{{0}} = '{{2}}';
var method{{0}} = eval('ObjC.classes["' + className{{0}} + '"]["' + methodName{{0}} + '"]');

var original_impl{{0}} = method{{0}}.implementation;
method{{0}}.implementation = ObjC.implement(method{{0}}, function(handle, selector{{3}}) {
	var original_result = original_impl{{0}}(handle, selector{{3}});

	send('Your code write here!!!');

	return original_result;
});
