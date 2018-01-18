var makeClickable = function() {
  var clickables = document.getElementsByClassName("clickable");

  for (var i = 0; i < clickables.length; i++) {
    clickables[i].addEventListener("click", function() {
      var i_id = this.parentElement.getAttribute("id");
      openItemModal(i_id);
      this.parentElement.style.boxShadow = "none";
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
      for (item in items) {
        if (document.getElementById(item) == null) {
          addItem(item);
        }
      }
      setSelectValues([]);
    }
  });

}

refreshButton.addEventListener("click", refresh);

var addItem = function(itemId) {
  $.ajax({
    url: '/api/get_item_template?i_id=' + itemId,
    type: 'GET',
    success: function(itemTemplate) {
      var listingCell = document.getElementById("listingCell");
      listingCell.innerHTML = itemTemplate + listingCell.innerHTML;
      var emptyText = document.getElementById("emptyText")
      if (emptyText != null) {
        emptyText.remove();
      }
      makeClickable();
    }
  });
}

var openItemModal = function(itemId) {
  $.ajax({
    url: '/api/get_item_modal?i_id=' + itemId,
    type: 'GET',
    success: function(itemTemplate) {
      var options = getSelectValues();
      document.getElementsByTagName("body")[0].innerHTML += itemTemplate;
      var itemModal = new Foundation.Reveal($('#item' + itemId));
      itemModal.open();
      $('#item' + itemId).foundation();
      makeClickable();
      makeSelectable();
      setSelectValues(options);
    }
  });
}

makeClickable();

var makeSelectable = function() {
  var selectFilter = document.getElementById("select_filters");
  selectFilter.addEventListener("change", function() {
    $.ajax({
      url: '/api/get_items_filters?filters=' + getSelectValues(),
      type: 'GET',
      success: function(items) {
        removeItems();
        items = JSON.parse(items);
        for (item in items) {
          addItem(item);
        }
      }
    });
  });
}

var getSelectValues = function() {
  var select = document.getElementById("select_filters");

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

var setSelectValues = function(selectedOptions) {
  var select = document.getElementById("select_filters");

  var options = select && select.options;
  var opt;

  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (selectedOptions.indexOf(opt.value) != -1) {
      opt.selected = true;
    } else {
      opt.selected = false;
    }
  }
}
