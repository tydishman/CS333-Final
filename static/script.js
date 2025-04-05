document.getElementById("openNav").addEventListener("click", w3_open);

function w3_open() {
  document.getElementById("main").style.marginLeft = "18%";
  const sidebar = document.getElementById("mySidebar");
  sidebar.style.width = "18%";
  sidebar.style.display = "block";
  document.getElementById("openNav").style.display = "none";
}

function w3_close() {
  document.getElementById("main").style.marginLeft = "0";
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("openNav").style.display = "inline-block";
}