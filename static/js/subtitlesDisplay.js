// Query all subs
var subtitlesDiv = document.getElementsByClassName('sub');

// Get settings
const afterSubtitles = 1;
const beforeSubtitles = 1;

// Amount in Miliseconds.
const handleMiliSeconds = 500;
const handleSeconds = handleMiliSeconds * 0.001;

var previousSubtitleBtn = document.getElementById('previousSubtitleBtn');
previousSubtitleBtn.addEventListener("click", goToPrevious);

var nextSubtitleBtn = document.getElementById('nextSubtitleBtn');
nextSubtitleBtn.addEventListener("click", goToNext );

var previousUnansweredSubtitleBtn = document.getElementById('previousUnansweredSubtitleBtn');
previousUnansweredSubtitleBtn.addEventListener("click", goToPreviousUnanswered);

var nextUnansweredSubtitleBtn = document.getElementById('nextUnansweredSubtitleBtn');
nextUnansweredSubtitleBtn.addEventListener("click", goToNextUnanswered );

document.getElementById('answer').addEventListener("click", ___answer);

// Add all eventListener to input
for (let i = 0; i < subtitlesDiv.length; i++) {
  subtitleDiv = subtitlesDiv[i];
  inputChildren = subtitleDiv.getElementsByClassName('inputSub');
}

function ___answer(){

  var visibleSubs = document.getElementsByClassName('visible');
  for (let i = 0; i < visibleSubs.length; i++){
    var childInputs = visibleSubs[i].getElementsByClassName("inputSub");

    for (let j = 0; j < childInputs.length; j++) {
      childInput = childInputs[j];
      childInput.classList.add('correctInput');
      childInput.classList.remove('incorrectInput');
    }
  }

  __setScoreStr();

}

function __goTo(inPrevious=false) {
  __clearIntervals();
  // Remove any visible subtitles.
  var visibleSubs = document.getElementsByClassName('visible');

  // If no current subtitle, go to next one todo!
  if (visibleSubs.length === 0)
    return;

  if (inPrevious){
    newSub = visibleSubs[0].previousElementSibling;
    tempSub = newSub;
    for (let i = 0; i < beforeSubtitles + 1; i++) {
      tempSub = tempSub.previousElementSibling;
      if (tempSub === null)
        break
      newSub = tempSub;
    }
  }

  else {
    newSub = visibleSubs[visibleSubs.length - 1].nextElementSibling;
    tempSub = newSub;
    for (let i = 0; i < afterSubtitles + 1; i++) {
      tempSub = tempSub.nextElementSibling;
      if (tempSub === null)
        break
      newSub = tempSub;
    }
  }

  subTime = parseFloat(newSub.dataset.start);

  __clearCurrentSubtitle();
  displaySubtitles(subTime);

  newVisibleSubs = document.getElementsByClassName('visible');
  var startTime = parseFloat(newVisibleSubs[0].dataset.start) - handleSeconds;
  timer = handleMiliSeconds

  player.seekTo(startTime);

  if (player.getPlayerState() === YT.PlayerState.PAUSED)
    player.playVideo();

}

function goToNext(){
  __goTo();
}

function goToPrevious(){
  __goTo(true);
}

function __goToUnanswered(inPrevious=false) {
  __clearIntervals();
  var visibleSubs = document.getElementsByClassName('visible');

  // If no current subtitle, go to next one todo!
  if (visibleSubs.length === 0)
    return;

  if (inPrevious){
    newSub = visibleSubs[0].previousElementSibling;

    while(newSub !== null){
      newSub = newSub.previousElementSibling;

      if (!__isChildCorrect(newSub))
        break;
    }

  }


  else {
    newSub = visibleSubs[visibleSubs.length - 1].nextElementSibling;

    while(newSub !== null){
      newSub = newSub.nextElementSibling;

      if (!__isChildCorrect(newSub))
        break;
    }

    }

  startTime = parseFloat(newSub.dataset.start);
  // Remove any visible subtitles
  for (let i = 0; i < visibleSubs.length; i++)
    visibleSubs[i].classList.remove('visible');

  __clearCurrentSubtitle();
  displaySubtitles(startTime);
  player.seekTo(startTime);

  if (player.getPlayerState() === YT.PlayerState.PAUSED)
    player.playVideo();

}

function goToNextUnanswered(){
  __goToUnanswered()
}

function goToPreviousUnanswered(){
  __goToUnanswered(true)
}

function __getSubFromTime(inTime){

  for (let i = 0; i < subtitlesDiv.length; i++) {

    subtitleDiv = subtitlesDiv[i]

    if (__isTimeBetweenRange(inTime, subtitleDiv))
      return subtitleDiv;
  }

  return null

}

function __isTimeBetweenRange(inCurrentTime, inDiv){
  // Return true if div dataset start and end are between the provided time.
  return (inCurrentTime >= inDiv.dataset.start && inCurrentTime <= inDiv.dataset.end)
}

function __isChildCorrect(inSub){

  childInputs = inSub.getElementsByClassName("inputSub");

  for (let j = 0; j < childInputs.length; j++) {

    childInput = childInputs[j];
    if (!(childInput.classList.contains('correctInput')))
      return false;

  }

  return true;

}

function __clearVisible(){
  document.querySelectorAll('.visible').forEach(e => e.classList.remove('visible'));
}

function __isChildAnswered(inSub){

  childInputs = inSub.getElementsByClassName("inputSub");

  for (let j = 0; j < childInputs.length; j++) {
    childInput = childInputs[j];
    if (childInput.value === '')
      return false;
  }

  return true;

}

function __swapLiveSubtitle(newCurrentSubtitle){
  let liveSubtitles = document.getElementsByClassName('live');

  if (liveSubtitles.length !== 0){
    if (newCurrentSubtitle === liveSubtitles[0])
      return;
  }

  for (let i = 0; i < liveSubtitles.length; i++) {
    liveSubtitles[i].classList.remove('live')
  }

  newCurrentSubtitle.classList.add('live');

}

function __swapCurrentSubtitle(currentSubtitle, newCurrentSubtitle){
  if (currentSubtitle !== null)
    currentSubtitle.id = '';

  newCurrentSubtitle.classList.add('visible');
  newCurrentSubtitle.id = 'current';
}

function __clearCurrentSubtitle(){
  var currentSubtitle = document.getElementById('current');

  if (currentSubtitle !== null)
    currentSubtitle.id = '';
}

function __isNeighbour(sourceSubtitle, newSubtitle) {
  return sourceSubtitle.nextElementSibling === newSubtitle;
}

function __setVisibleNeighbours(inRange,
                                inCurrentSub,
                                inIsBefore = false){

  var tempSub = inCurrentSub;

  // Display subtitles before/after.
  for (let i = 1; i < inRange + 1; i++){

    if (inIsBefore)
      newSub = tempSub.previousElementSibling;
    else
      newSub = tempSub.nextElementSibling;

    if (newSub === null)
      return;

    if (!newSub.classList.contains('sub'))
      return;

    newSub.classList.add('visible');
    tempSub = newSub;
  }
}

function displaySubtitles(inCurrentTime=player.getCurrentTime()) {

  // Function to display subtitles based on the current settings.
  var newCurrentSubtitle = __getSubFromTime(inCurrentTime);

  // If no sub from time, no need to do any display calls.
  if (newCurrentSubtitle === null)
    return;

  var currentSubtitle = document.getElementById('current');

  // If same subtitle, no need to display anything new!
  if (currentSubtitle === newCurrentSubtitle)
    return

  // Remove any visible subtitles
  __clearVisible();

  __swapCurrentSubtitle(currentSubtitle, newCurrentSubtitle);

  // Display subtitles before.
  __setVisibleNeighbours(
      beforeSubtitles,
      newCurrentSubtitle,
      true);

  // Display subtitles after.
  __setVisibleNeighbours(
      afterSubtitles,
      newCurrentSubtitle,
      false);

}

function mainSubtitles(){
  var currentTime = player.getCurrentTime();
  var newCurrentSubtitle = __getSubFromTime(currentTime);

  if (newCurrentSubtitle === null)
    return;

  __swapLiveSubtitle(newCurrentSubtitle);

  var visibleSubs = Array.from(document.getElementsByClassName('visible'));
  var visibleSubsLength = visibleSubs.length

  if (visibleSubsLength === 0){
    displaySubtitles(currentTime);
    return;
  }

  var isVisible = visibleSubs.includes(newCurrentSubtitle);

  // In case user fast forwards on youtube video player.
  if (!isVisible && !__isNeighbour(visibleSubs[visibleSubs.length - 1], newCurrentSubtitle)){
    displaySubtitles(currentTime);
    return;
    }

  var endTime = parseFloat(visibleSubs[visibleSubsLength - 1].dataset.end);
  var startTime = parseFloat(visibleSubs[0].dataset.start) - handleSeconds;

  if (currentTime > endTime) {
    __clearIntervals();
    timer = 500;
    player.pauseVideo();
    player.seekTo(startTime);
  }

}
