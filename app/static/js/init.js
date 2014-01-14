$(document).ready(function(){
	$('#whiskies div.chart').each(function(){
	
		// get data					
		reference = $('th.reference', this).html()
		whisky = $('th.whisky', this).html()
		tastes_whisky = new Array()
		tastes_reference = new Array()
		count = 0
		$('td', this).each(function(){
			if ( count % 2 == 0 ) {
				tastes_whisky.push(parseInt($(this).html()))	
			} else { 
				tastes_reference.push(parseInt($(this).html()))
			}
			count++
		})
		categories = new Array()
		count = 0
		$('th', this).each(function(){
			if ( count > 2 ) { 
				categories.push($(this).html())
			}
			count++
		})
		
		// remove table and add chart
		$('table', this).remove()
		$(this).append(document.createElement('div'))
		$('div', this).highcharts({
			chart: {
				polar: true,
				type: 'area',
				height: 300,
				backgroundColor: '#ffffff',
				animation: false
			},
			plotOptions: {
				area: {
					animation: false,
					lineWidth: 1,
					fillOpacity: 0.6,
					enableMouseTracking: false,
					marker: {
						enabled: false
					}
				}
			},
			colors : ['#cecece', '#3375B4'],
			title: {
				text: null,
			},
			pane: {
				size: '70%'
			},
			xAxis: {
				categories: categories,
				tickmarkPlacement: 'on',
				lineWidth: 0
			},
			yAxis: {
				gridLineInterpolation: 'polygon',
				lineWidth: 0,
				min: 0,
				max: 4,
				tickInterval: 1,
				labels : {
					enabled: false
				}
			},
			tooltip: {
				enabled: false
			},
			legend: {
				enabled: false
			},  
			series: [{
				name: reference,
				data: tastes_reference,
			}, {
				name: whisky,
				fillOpacity: 0.1,
				data: tastes_whisky
			}]
	
		}) // close highcharts()
		
	}) // close each()

	// autocomplete
	$('#s').typeahead({
		name: 'whiskyton',
		limit: 36,
		prefetch: 'whiskyton.json'
	})

}) // close ready()
