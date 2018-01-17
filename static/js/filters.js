var select_filter = document.getElementById("select_filters");

select_filter.addEventListener("change", function() {
  $.ajax({
    url: '/api/get_items_filters?filters=' + getSelectValues(select_filter),
    type: 'GET',
    success: function() {
      console.log("Success!");
    }
  });
});

function getSelectValues(select) {
  var result = [];
  var options = select && select.options;
  var opt;

  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (opt.selected) {
      result.push(opt.value || opt.text);
    }

  }
  return result;
}
