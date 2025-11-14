var video = document.getElementById("myVideo");
var playButton = document.getElementById("playButton");
  document.getElementById("playButton").addEventListener("click", function() {
    video.style.display = "block";
    video.requestFullscreen();
    video.play();
  });

  document.getElementById("myVideo").addEventListener("ended", function() {
    video.style.display = "none";
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  });

document.addEventListener("keyup", function(event) {
  if (event.code === "KeyP") {
    video.paused ? video.play() : video.pause();
  } else if (event.code === "KeyS") {
    document.exitFullscreen();
  }else if (event.code === "KeyR") {
    video.currentTime = 0;
  }
});

document.addEventListener("keydown", function(event) {
  var volumeDisplay = document.getElementById("volumeDisplay");
  if (event.code === "Minus") {
    if (video.volume > 0) {
      video.volume -= 0.1;
    }
  } else if (event.code === "Equal") {
    if (video.volume < 1) {
      video.volume += 0.1;
    }
  }
  volumeDisplay.innerHTML = "Volume: " + (video.volume * 100).toFixed(0) + "%";
});

document.addEventListener("fullscreenchange", function() {
  if (document.fullscreenElement) {
    document.body.style.pointerEvents = "none";
  } else {
    document.body.style.pointerEvents = "auto";
    video.pause();
    video.currentTime = 0;
    video.style.display = "none";
    document.body.style.cursor = "default";
    document.body.style.pointerEvents = "auto";
  }
});