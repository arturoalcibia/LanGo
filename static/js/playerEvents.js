var intervals = [];

function onStateChange(event) {

  var playerState = event.data;

    if (playerState === YT.PlayerState.PLAYING) {

      intervals.push(setInterval(displaySubtitles, 100));

    }
    else {
        for (let i = 0; i < intervals.length; i++) { clearInterval( intervals[i] ); }
    }

}