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
