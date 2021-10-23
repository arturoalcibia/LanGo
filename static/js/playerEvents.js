// Connect speed radio buttons.
speedRadioBtns = document.getElementsByName('speedRadio')
document.getElementById('oneRadio').checked = true;
for(radio in speedRadioBtns) {
    speedRadioBtns[radio].onclick = function() {
        player.setPlaybackRate(parseFloat(this.value));
    }
}

var intervals = [];

// Player will restore the subtitles interval after the timer has timed out.
var timer = 0;

function __clearIntervals(){
  for (let i = 0; i < intervals.length; i++) { clearInterval( intervals[i] ); }
}

function __restoreInterval(inAfterXMiliSeconds=0){
  setTimeout(function () {
        intervals.push(setInterval(mainSubtitles, 100));
        timer = 0;
    }, inAfterXMiliSeconds);
}

function onStateChange(event) {

  var playerState = event.data;

    if (playerState === YT.PlayerState.PLAYING) {
      __restoreInterval(timer)

    }
    else {
        __clearIntervals();
    }

}