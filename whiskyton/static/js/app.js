$(document).ready(function () {
  $.getJSON('/whiskyton.json', function(data) {
      $('#s').autocomplete({lookup: data.whiskies})
  });
});
