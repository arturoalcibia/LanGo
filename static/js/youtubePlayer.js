var startSeconds = 4.5;
var endSeconds = 5;
var firstTime = true;

var playPauseButton = document.getElementById("playPauseButton");
var isLoopCheckBox  = document.getElementById("isLoop");

var player;

var playerConfig = {
  height: '360',
  width: '640',
  videoId: videoId,
  playerVars: {
    autoplay: 0, // Auto-play the video on load
    mute: 0, // Auto-play the video on loa
    controls: 0, // Show pause/play buttons in player
    showinfo: 0, // Hide the video title
    modestbranding: 1, // Hide the Youtube Logo
    rel: 0, // Hide related videos on pause/end video
    fs: 1, // Hide the full screen button
    cc_load_policy: 1, // Hide closed captions
  	cc_lang_pref: 'fr',
    iv_load_policy: 3, // Hide the Video Annotations
    start: startSeconds,
    end: endSeconds,
    autohide: 0, // Hide video controls when playing
  },
  events: {
    'onStateChange': onStateChange,
  }
};

function onYouTubePlayerAPIReady() {
  player = new YT.Player('ytplayer', playerConfig);
}


function onStateChange(event) {

  var playerState = event.data;

	if (playerState === YT.PlayerState.PLAYING) {

    if (firstTime){
  	firstTime = false;
  	playPauseButton.style.visibility = 'visible';
  }

    switchButton(switchToPlay=false);
  }

	else if (playerState === YT.PlayerState.PAUSED) {
    switchButton(switchToPlay=true);
  }

  if (playerState === YT.PlayerState.ENDED) {

  	if (isLoopCheckBox.checked) { player.playVideo(); }
    else { switchButton(switchToPlay=true); }

  }
}

function switchButton(switchToPlay) {

  if (switchToPlay) {
    playPauseButton.innerHTML = 'Play';
    playPauseButton.onclick = function() { player.playVideo(); };
  }

  else{
  	playPauseButton.innerHTML = 'Pause';
    playPauseButton.onclick = function() { player.pauseVideo(); };
  }
}

// Inject YouTube API script
var tag = document.createElement("script");
tag.src = "//www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);