var makeClickable = function() {
  var clickables = document.getElementsByClassName("clickable");

  for (var i = 0; i < clickables.length; i++) {
    clickables[i].addEventListener("click", function() {
      alert(this.parentElement.getAttribute("id"));
    });
    clickables[i].addEventListener("mouseover", function() {
      this.parentElement.style.boxShadow = "5px 10px 15px black";
    });
    clickables[i].addEventListener("mouseleave", function() {
      this.parentElement.style.boxShadow = "none";
    });
  }
}

var refreshButton = document.getElementById("refresh");

var refresh = function() {

  $.ajax({
    url: '/api/get_items',
    type: 'GET',
    success: function(items) {
      items = JSON.parse(items);
      console.log(items);
      for (item in items) {
        if (document.getElementById(item) == null) {
          console.log(items[item]);
          addItem(item);
        }
      }
    }
  });

}

refreshButton.addEventListener("click", refresh);

var listingCell = document.getElementById("listingCell");

var addItem = function(itemId) {
  $.ajax({
    url: '/api/get_item_template?i_id=' + itemId,
    type: 'GET',
    success: function(itemTemplate) {
      listingCell.innerHTML = itemTemplate + listingCell.innerHTML;
      document.getElementById("emptyText").remove();
      makeClickable();
    }
  });
}

makeClickable();
