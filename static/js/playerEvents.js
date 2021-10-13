// Connect speed radio buttons.
speedRadioBtns = document.getElementsByName('speedRadio')
document.getElementById('oneRadio').checked = true;
for(radio in speedRadioBtns) {
    speedRadioBtns[radio].onclick = function() {
        player.setPlaybackRate(parseFloat(this.value));
    }
}

var intervals = [];

function __clearIntervals(){
  for (let i = 0; i < intervals.length; i++) { clearInterval( intervals[i] ); }
}

function onStateChange(event) {

  var playerState = event.data;

    if (playerState === YT.PlayerState.PLAYING) {
      intervals.push(setInterval(mainSubtitles, 100));

    }
    else {
        __clearIntervals();
    }

}