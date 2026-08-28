(function () {
  "use strict";

  var audio = document.getElementById("audio");
  var playBtn = document.getElementById("playBtn");
  var disc = document.getElementById("disc");
  var range = document.getElementById("seek");
  var fill = document.getElementById("progressFill");
  var knob = document.getElementById("progressKnob");
  var currentTimeEl = document.getElementById("currentTime");
  var durationEl = document.getElementById("duration");

  if (!audio) return;

  function formatTime(seconds) {
    if (!isFinite(seconds) || isNaN(seconds)) return "0:00";
    var m = Math.floor(seconds / 60);
    var s = Math.floor(seconds % 60);
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function setPlayingState(isPlaying) {
    playBtn.classList.toggle("is-playing", isPlaying);
    disc.classList.toggle("is-playing", isPlaying);
    playBtn.setAttribute("aria-label", isPlaying ? "Pausar" : "Reproducir");
  }

  function updateProgress() {
    var pct = 0;
    if (audio.duration) {
      pct = (audio.currentTime / audio.duration) * 100;
    }
    range.value = pct;
    fill.style.width = pct + "%";
    knob.style.left = pct + "%";
    currentTimeEl.textContent = formatTime(audio.currentTime);
  }

  playBtn.addEventListener("click", function () {
    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
  });

  audio.addEventListener("play", function () {
    setPlayingState(true);
  });

  audio.addEventListener("pause", function () {
    setPlayingState(false);
  });

  audio.addEventListener("ended", function () {
    setPlayingState(false);
    audio.currentTime = 0;
    updateProgress();
  });

  audio.addEventListener("loadedmetadata", function () {
    durationEl.textContent = formatTime(audio.duration);
  });

  audio.addEventListener("timeupdate", updateProgress);

  range.addEventListener("input", function () {
    if (audio.duration) {
      var time = (range.value / 100) * audio.duration;
      audio.currentTime = time;
      updateProgress();
    }
  });
})();
