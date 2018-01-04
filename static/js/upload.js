// Attach the change event listener to change the label of all input[type=file] elements
var els = document.querySelectorAll("input[type=file]"),
    i;
for (i = 0; i < els.length; i++) {
  els[i].addEventListener("change", function() {
    var filenames = document.getElementById("filenames");
    if (filenames.innerHTML != "") {
      filenames.innerHTML += ", ";
    }
    filenames.innerHTML += this.files[0].name;
  });

}
