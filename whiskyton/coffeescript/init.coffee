$(document).ready ->
  $.getJSON '/whiskyton.json',
    (data) ->
      $('#s').autocomplete {lookup: json2array data.whiskies}

json2array = (data) ->
  values = []
  $.each(data, (key, val) -> values.push val)
  values
