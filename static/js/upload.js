var els = document.querySelectorAll("input[type=file]"), i;
for (i = 0; i < els.length; i++) {
  els[i].addEventListener("change", function() {
    var filenames = document.getElementById("filenames");
    filenames.innerHTML = "";

    for (var i = 0; i < this.files.length; i++) {
      if (filenames.innerHTML != "") {
        filenames.innerHTML += ", ";
      }
      filenames.innerHTML += this.files[i].name;
    }
  });

}
