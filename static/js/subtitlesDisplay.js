// Notes:
// todo:
//  get back startTime function on not loop all, maybe just loop one subtitle less.
//  bug: when answering and on loop mode, sometimes 4 subs are displayed.
//

// Query all subs
var subtitlesDiv = document.getElementsByClassName('sub');

// Get settings
var beforeSettingsInput = document.getElementById("beforeSettingsInput");
beforeSettingsInput.value = 1;
beforeSettingsInput.addEventListener('input', refreshSubtitles);
var afterSettingsInput  = document.getElementById("afterSettingsInput");
afterSettingsInput.value = 1;
afterSettingsInput.addEventListener('input', refreshSubtitles);

document.getElementById('loopCorrectRadio').checked = true;

var previousSubtitleBtn = document.getElementById('previousSubtitleBtn');
previousSubtitleBtn.addEventListener("click", goToPrevious);

var nextSubtitleBtn = document.getElementById('nextSubtitleBtn');
nextSubtitleBtn.addEventListener("click", goToNext );

const noLoopRadio = 0
const loopOnceRadio = 1
const loopCorrectRadio = 2
const loopAnsweredRadio = 3

// Add all eventListener to input
for (let i = 0; i < subtitlesDiv.length; i++) {
  subtitleDiv = subtitlesDiv[i];
  inputChildren = subtitleDiv.getElementsByClassName('inputSub');
}

function __goTo(inPrevious=false) {
  __clearIntervals();
  // Remove any visible subtitles.
  var visibleSubs = document.getElementsByClassName('visible');
  // Remove any visible subtitles
  for (let i = 0; i < visibleSubs.length; i++)
    visibleSubs[i].classList.remove('visible');

  // If no current subtitle, go to next one todo!
  if (visibleSubs.length === 0)
    return;

  if (inPrevious){
    newSub = visibleSubs[0].previousElementSibling;

    tempSub = newSub;
    for (let i = 0; i < parseInt(beforeSettingsInput.value) + 1; i++) {

      tempSub = tempSub.previousElementSibling;

      if (tempSub === null)
        break

      newSub = tempSub;

    }

  }

  else {
    newSub = visibleSubs[visibleSubs.length - 1].nextElementSibling;

    tempSub = newSub;
    for (let i = 0; i < parseInt(afterSettingsInput.value) + 1; i++) {

      tempSub = tempSub.nextElementSibling;

      if (tempSub === null)
        break

      newSub = tempSub;

    }
  }

  startTime = parseFloat(newSub.dataset.start);
  // Remove any visible subtitles
  for (let i = 0; i < visibleSubs.length; i++)
    visibleSubs[i].classList.remove('visible');

  __clearCurrentSubtitle();
  displaySubtitles(startTime);
  player.seekTo(startTime);

}

function goToNext(){
  __goTo();
}

function goToPrevious(){
  __goTo(true);
}

function __clearVisible(subToSkip){
  // Remove any visible subtitles.
  var visibleSubs = document.getElementsByClassName('visible');
  for (let i = 0; i < visibleSubs.length; i++){

    visibleSub = visibleSubs[i];

    // Omit the current sub.
    if (visibleSub === subToSkip)
      continue

    visibleSub.classList.remove('visible');
  }
}

function __getSubFromTime(inTime){

  for (let i = 0; i < subtitlesDiv.length; i++) {

    subtitleDiv = subtitlesDiv[i]

    if (__isTimeBetweenRange(inTime, subtitleDiv))
      return subtitleDiv;
  }

  return null

}

function __getStartTime(inSubs) {
  // Check if visible subtitles have been answered to define if subtitles should change!
  for (let i = 0; i < inSubs.length; i++)
    return inSubs[i].dataset.start;
}

function __getEndTime(inSubs){

  if (inSubs.length === 1)
    return inSubs[0].dataset.end;

  return inSubs[inSubs.length - 1].dataset.end;
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

function __isChildAnswered(inSub){

  childInputs = inSub.getElementsByClassName("inputSub");

  for (let j = 0; j < childInputs.length; j++) {
    childInput = childInputs[j];
    if (childInput.value === '')
      return false;
  }

  return true;

}

function __isChildrenCorrect(inSubs) {
  for (let i = 0; i < inSubs.length; i++) {
    visibleSub = inSubs[i];
    if (!__isChildCorrect(visibleSub))
      return false
  }
  return true
}

function __isChildrenAnswered(inSubs) {
  for (let i = 0; i < inSubs.length; i++) {
    visibleSub = inSubs[i];
    if (!__isChildAnswered(visibleSub))
      return false
  }
  return true
}


function __swapCurrentSubtitle(currentSubtitle, newCurrentSubtitle){

  // If any current sub already, unset them to set the new one.
  //todo! add a note that for a first time, current sub could be null
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


function __setVisibleNeighbours(inRange,
                                inCurrentSub,
                                inIsBefore = false){

  if (inRange === 0)
    return

  tempSub = inCurrentSub;

  // Display subtitles before/after.
  for (let i = 1; i < inRange; i++){

    if (inIsBefore)
      newSub = tempSub.previousElementSibling;
    else
      newSub = tempSub.nextElementSibling;

    if (newSub === null)
      return;

    newSub.classList.add('visible');
    tempSub = newSub;
  }
}

function displaySubtitles(inCurrentTime=player.getCurrentTime()) {
  // Called on an interval.
  // Function to display subtitles based on the current settings.

  var newCurrentSubtitle = __getSubFromTime(inCurrentTime);

  // If no sub from time, no need to do any display calls.
  if (newCurrentSubtitle === null)
    return;

  var currentSubtitle = document.getElementById('current');
  var visibleSubs = document.getElementsByClassName('visible');

  // Remove any visible subtitles
  for (let i = 0; i < visibleSubs.length; i++)
    visibleSubs[i].classList.remove('visible');

  __swapCurrentSubtitle(currentSubtitle, newCurrentSubtitle);

  // Display subtitles before.
  __setVisibleNeighbours(
      (parseInt(beforeSettingsInput.value) + 1),
      newCurrentSubtitle,
      true);

  // Display subtitles after.
  __setVisibleNeighbours(
      parseInt(afterSettingsInput.value) + 1,
      newCurrentSubtitle,
      false);

}

function mainSubtitles(){

  var visibleSubs = document.getElementsByClassName('visible');

  if (visibleSubs.length === 0){
    displaySubtitles();
    return;
  }

  var loopStateInt = parseInt(document.querySelector('input[name="loop"]:checked').value);

  if (loopStateInt !== noLoopRadio) {

    var currentTime = player.getCurrentTime()
    var endTime = __getEndTime(visibleSubs);
    var startTime = __getStartTime(visibleSubs);

    if (loopStateInt === loopOnceRadio) {

      if (currentTime > endTime) {
        __clearIntervals();
        player.pauseVideo();
        player.seekTo(startTime);
        return;
      }
    }

    else if (loopStateInt === loopCorrectRadio){

      if (currentTime > endTime) {
        if (__isChildrenCorrect(visibleSubs)){
          displaySubtitles();
          return;
        }

        player.seekTo(startTime);

      }
    }

    else if (loopStateInt === loopAnsweredRadio){

      if (currentTime > endTime) {

        if (__isChildrenCorrect(visibleSubs)){
          displaySubtitles();
          return;
        }

        player.seekTo(startTime);

      }
    }

    }

    else
      displaySubtitles();

}

function refreshSubtitles() {

  var currentSubtitle = document.getElementById('current');

  // No subtitles to display.
  if (currentSubtitle === null)
    return

  // Remove any visible subtitles.
  __clearVisible(currentSubtitle);

  // Display subtitles before.
  __setVisibleNeighbours(
      (parseInt(beforeSettingsInput.value) + 1),
      currentSubtitle,
      true);

  // Display subtitles after.
  __setVisibleNeighbours(
      parseInt(afterSettingsInput.value) + 1,
      currentSubtitle,
      false);
}
