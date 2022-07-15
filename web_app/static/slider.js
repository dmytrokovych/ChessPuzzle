function slider_update() {
  var slider = document.querySelector(".slider");
  var games_number = document.getElementById("games_number");

  games_number.value = slider.value;

  slider.oninput = function () {
    games_number.value = slider.value;
  };
}

window.onload = slider_update;
