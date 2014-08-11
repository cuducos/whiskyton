$(document).ready(function(){	
	$.getJSON( "/whiskyton.json", function( data ) {
		var whiskies = json2array(data);
		$('#s').autocomplete({lookup: whiskies});
	});
});

var json2array = function (data) {
	var values = [];
	$.each(data, function(key, val) {
		values.push(val);
	});
	return values;
}
