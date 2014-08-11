$(document).ready(function(){

	// typeahed + bloodhound
	var whiskies = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		limit: 10,
		prefetch: {
			url: '/whiskyton.json'		
		}
	});
	whiskies.initialize();
	$('#s').typeahead(null, {
		name: 'whiskies',
		displayKey: 'name',
		source: whiskies.ttAdapter()
	});
	
});

	
