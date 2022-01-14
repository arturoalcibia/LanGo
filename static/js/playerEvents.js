// Query divs to hide before playing.
const scoreDiv = document.getElementById('scoreDiv');
const hideBtnDiv = document.getElementById('hideBtnDiv');
const buttonsDiv = document.getElementById('buttonsDiv');
const settingsDiv = document.getElementById('settingsDiv');

const ytPlayerDiv = document.getElementById('ytplayerdiv');

const divsToHide = [scoreDiv, hideBtnDiv, buttonsDiv, settingsDiv]

const InitialInstructionDiv = document.getElementById('InitialInstructionDiv');

var firstTimePlaying = true;

for (let i = 0; i < divsToHide.length; i++) {
  divsToHide[i].classList.add('hidden')
}

var hideButton = document.getElementById('hideVideoBtn');
hideButton.addEventListener("click", hideVideo);

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

        if (firstTimePlaying){
            for (let i = 0; i < divsToHide.length; i++) {
                divsToHide[i].classList.remove('hidden');
            }
            InitialInstructionDiv.classList.add('hidden');
            hideVideo()
            player.seekTo(0);
            firstTimePlaying = false;
        }

      __restoreInterval(timer)

    }
    else {
        __clearIntervals();
    }

}

function hideVideo(){
    if (ytPlayerDiv.classList.contains('hidden'))
        ytPlayerDiv.classList.remove('hidden')
    else
        ytPlayerDiv.classList.add('hidden')
}