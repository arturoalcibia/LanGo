var player;

var playerConfig = {
  height: '360',
  width: '640',
  videoId: videoId,
  playerVars: {
    autoplay: 0, // Auto-play the video on load
    mute: 0, // Auto-play the video on loa
    controls: 1, // Show pause/play buttons in player
    showinfo: 0, // Hide the video title
    modestbranding: 1, // Hide the Youtube Logo
    rel: 0, // Hide related videos on pause/end video
    fs: 1, // Hide the full screen button
    cc_load_policy: 1, // Hide closed captions
  	cc_lang_pref: 'fr',
    iv_load_policy: 3, // Hide the Video Annotations
    start: 0,
    autohide: 0, // Hide video controls when playing
  },
  events: {
    'onStateChange': onStateChange,
  }
};

function onYouTubePlayerAPIReady() {
  player = new YT.Player('ytplayer', playerConfig);
}

// Inject YouTube API script
var tag = document.createElement("script");
tag.src = "//www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);