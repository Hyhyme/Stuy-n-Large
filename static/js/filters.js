makeSelectable();

var removeItems = function() {
  var listingCell = document.getElementById("listingCell");
  listingCell.innerHTML = "";
}

var queryInput = document.getElementById("queryInput");

queryInput.value = window.location.search.substring(7);
