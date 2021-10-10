// Query all subs
var subtitlesDiv = document.getElementsByClassName('sub');

// Get settings
var beforeSettingsInput = document.getElementById("beforeSettingsInput");
beforeSettingsInput.value = 0;
beforeSettingsInput.addEventListener('input', refreshSubtitles);
var afterSettingsInput  = document.getElementById("afterSettingsInput");
afterSettingsInput.value = 1;
afterSettingsInput.addEventListener('input', refreshSubtitles);
var loopCorrectCheckBox = document.getElementById('loopCorrectCheckBox');
loopCorrectCheckBox.checked = true;
var loopAnsweredCheckBox = document.getElementById('loopAnsweredCheckBox');
loopAnsweredCheckBox.checked = true;
var skipAnsweredCheckBox = document.getElementById('skipAnsweredCheckBox');
skipAnsweredCheckBox.checked = true;

// Global vars:
var lastSeekedSub = null;

// Add all eventListener to input
for (let i = 0; i < subtitlesDiv.length; i++) {
  subtitleDiv = subtitlesDiv[i];
  inputChildren = subtitleDiv.getElementsByClassName('inputSub');
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

function __getStartTime(inSubs, skipAnswered = false, skipCorrect = false) {
  // Check if visible subtitles have been answered to define if subtitles should change!
  for (let i = 0; i < inSubs.length; i++) {

    inSub = inSubs[i];

    if (skipAnswered && __isChildrenAnswered(inSub))
      continue

    else if (skipCorrect && __isChildrenCorrect(inSub))
      continue

    return inSub.dataset.start;
  }

  return null
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

function __isChildrenCorrect(inSub){

  childInputs = inSub.getElementsByClassName("inputSub");
  isChildrenCorrect = true;

  for (let j = 0; j < childInputs.length; j++) {
    childInput = childInputs[j];
    if (!(childInput.classList.contains('correctInput')))
    {
      isChildrenCorrect = false;
      break;
    }
  }
  return isChildrenCorrect;

}

function __isChildrenAnswered(inSub){

  childInputs = inSub.getElementsByClassName("inputSub");
  isChildrenAnswered = true;

  for (let j = 0; j < childInputs.length; j++) {
    childInput = childInputs[j];
    if (childInput.value === '')
    {
      isChildrenAnswered = false;
      break;
    }
  }
  return isChildrenAnswered;

}

function __isEmptyInput(inSubs) {

  // Check if visible subtitles have been answered to define if subtitles should change!
  for (let i = 0; i < inSubs.length; i++) {

    childInputs = inSubs[i].getElementsByClassName("inputSub");

    for (let j = 0; j < childInputs.length; j++) {
      childInput = childInputs[j];

      if (childInput.value == '')
        return true;
    }
  }
  return false;
}

function __isFocusedOnInput(){
  isInput = false;
  focusedElement = document.activeElement
  if (focusedElement.tagName === 'INPUT')
    isInput = true;

  return isInput;
}

function __isIncorrectInputs(inSubs){

  // Check if visible subtitles have been answered to define if subtitles should change!
  for (let i = 0; i < inSubs.length; i++){

    childInputs = inSubs[i].getElementsByClassName("inputSub");

    for (let j = 0; j < childInputs.length; j++) {
      childInput = childInputs[j];

      if (childInput.classList.contains('incorrectInput'))
      {
        return false;
        break;
      }
    }
  }

  return true

}

function __SwapCurrentSubtitle(currentSubtitle, newCurrentSubtitle){

  // If any current sub already, unset them to set the new one.
  //todo! add a note that for a first time, current sub could be null
  if (currentSubtitle !== null)
    currentSubtitle.id = '';

    newCurrentSubtitle.classList.add('visible');
    newCurrentSubtitle.id = 'current';
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

function displaySubtitles() {
  // Called on an interval.
  // Function to display subtitles based on the current settings.
  currentTime = player.getCurrentTime();

  var newCurrentSubtitle = __getSubFromTime(currentTime);

  // If no sub from time, no need to do any display calls.
  if (newCurrentSubtitle === null)
    return;

  // If looped, in case player.seekTo call was to start plus some handles.
  // Skip displaying any subtitles before the last start.
  if (lastSeekedSub !== null){
    if (newCurrentSubtitle !== lastSeekedSub)
      return;

    lastSeekedSub = null;
  }

  var currentSubtitle = document.getElementById('current');
  var visibleSubs = document.getElementsByClassName('visible');

  if ((loopAnsweredCheckBox.checked || loopCorrectCheckBox.checked) && visibleSubs.length > 0){

    if (loopAnsweredCheckBox.checked)
      var startTime = __getStartTime(visibleSubs, skipAnsweredCheckBox.checked);
    else if (loopCorrectCheckBox.checked)
      var startTime = __getStartTime(visibleSubs, undefined, skipAnsweredCheckBox.checked);

    // If already all answered subs, skip to next, no need to loop!
      if (startTime !== null){

        var endTime = __getEndTime(visibleSubs);

        if (currentTime > endTime){
          // Skip any already answered subtitles.
          player.seekTo(startTime - 0.500);
          // Keep reference of last seeked sub to avoid handles displaying any extra subtitle.
          lastSeekedSub = newCurrentSubtitle;
          return
        }

        if (currentSubtitle !== newCurrentSubtitle)
          return;

      }

  }

  // Remove any visible subtitles
  for (let i = 0; i < visibleSubs.length; i++)
    visibleSubs[i].classList.remove('visible');

  __SwapCurrentSubtitle(currentSubtitle, newCurrentSubtitle);

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
