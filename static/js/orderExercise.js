var firstTimePlaying = true;
var intervals = [];

var endAt = null;
var currentIndex = null;
var currentSentenceSplitted = [];

var player;

var playerConfig = {
  videoId: videoId,
  playerVars: {
    autoplay: 0, // Auto-play the video on load
    mute: 0, // Auto-play the video on loa
    controls: 1, // Show pause/play buttons in player
    showinfo: 0, // Hide the video title
    modestbranding: 1, // Hide the Youtube Logo
    rel: 1, // Hide related videos on pause/end video
    fs: 1, // Hide the full screen button
    cc_load_policy: 1, // Hide closed captions
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

function __clearIntervals(){
  for (let i = 0; i < intervals.length; i++) { clearInterval( intervals[i] ); }
}

function __restoreInterval(inAfterXMiliSeconds=0){
  setTimeout(function () {
        intervals.push(setInterval(stopVideoAtEnd, 100));
    }, inAfterXMiliSeconds);
}

function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function onStateChange(event) {

  var playerState = event.data;

  if (playerState === YT.PlayerState.PLAYING) {

      if (firstTimePlaying) {
          document.getElementById('InitialInstructionDiv').classList.add('hidden');
          document.getElementById('ytplayerdiv').classList.add('hidden');
          document.getElementById('words').classList.remove('hidden');
          firstTimePlaying = false;
          setSubtitle();
      }

   __restoreInterval(500)

    }
    else {
        __clearIntervals();
    }

}

function stopVideoAtEnd(){

    if (player.getCurrentTime() >= endAt){
        player.pauseVideo();
        endAt = null;
    }
}

function setSubtitle(inCurrentIndex=null) {

    // Set first subtitle to play.
    if (inCurrentIndex === null){
      inCurrentIndex = 0;
    }

    newCurrentSubtitle = subtitles[inCurrentIndex]
    currentIndex = inCurrentIndex;

    player.seekTo(newCurrentSubtitle['start']);

    if (player.state !== YT.PlayerState.PLAYING){
        player.playVideo();
    }

    endAt = newCurrentSubtitle['end'];

    destination.innerHTML = "";
    origin.innerHTML = "";

    var words = newCurrentSubtitle['text'].split(' ')
    currentSentenceSplitted =  [...words];
    shuffle(words);

    words.forEach(function (wordStr, index) {

      let wordDiv = document.createElement("div");
      wordDiv.classList.add('container');

      let wordSpan = document.createElement("span");
      wordSpan.textContent = wordStr;
      wordSpan.dataset.index = index;
      wordSpan.classList.add('word');
      wordSpan.classList.add('wordNeutral');

      wordDiv.append(wordSpan);
      origin.append(wordDiv);

      origin.querySelectorAll(".word").forEach((word) => { convert(word); });

    });

}

document.getElementById('skipBtn').onclick = function () {
    currentIndex = currentIndex + 1;
    setSubtitle(currentIndex);
};

document.getElementById('playBtn').onclick = function () {
    endAt = subtitles[currentIndex]['end']
    player.seekTo(subtitles[currentIndex]['start']);
    player.playVideo();
};

document.getElementById('checkBtn').onclick = function () {

    const words = destination.querySelectorAll(".word");

    words.forEach(function (wordSpan, index) {

        wordSpan.className = 'word';
        console.log(currentSentenceSplitted)

        const wordStr = wordSpan.textContent;

        if (wordStr === currentSentenceSplitted[index]){
            wordSpan.classList.add('wordCorrectOrder')
        }
        else if (currentSentenceSplitted.includes(wordStr)){
            wordSpan.classList.add('wordIncorrectOrder')
        }
        else {
            wordSpan.classList.add('wordIncorrect')
        }

    });

};