// Query all subs
var subtitlesDiv = document.getElementsByClassName('sub');

// Get settings
var beforeSettingsInput = document.getElementById("beforeSettingsInput");
beforeSettingsInput.value = 1
beforeSettingsInput.addEventListener('input', refreshSubtitles);
var afterSettingsInput  = document.getElementById("afterSettingsInput");
afterSettingsInput.value = 1
afterSettingsInput.addEventListener('input', refreshSubtitles);

var loopUntilCheckBox = document.getElementById('loopCheckBox');
loopUntilCheckBox.checked = true;

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

function __isTimeBetweenRange(inCurrentTime, inDiv){
  // Return true if div dataset start and end are between the provided time.
  return (inCurrentTime >= inDiv.dataset.start && inCurrentTime <= inDiv.dataset.end)
}

function __setVisibleNeighbours(inRange, inCurrentSub, inIsBefore){
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

function displaySubtitles(){
  // Called on an interval.
  // Function to display subtitles based on the current settings.
  currentTime = player.getCurrentTime();
  var currentIndex   = null;

  for (let i = 0; i < subtitlesDiv.length; i++) {

    subtitleDiv = subtitlesDiv[i]

    if (__isTimeBetweenRange(currentTime, subtitleDiv))
    {
      currentIndex = i;
      break;
    }
  }

  if (currentIndex !== null){

    // Check if subtitles need to change or looped over.
    var changeSubsBool = true;
    var previousCurrentSubtitle = document.getElementById('current');
    var visibleSubs = document.getElementsByClassName('visible');

    if (loopUntilCheckBox.checked && previousCurrentSubtitle !== null){
      changeSubsBool = false;

      // Set video current time.
      // if settings are only one visible video.
      if (visibleSubs.length === 1){
        startTime = visibleSubs[0].dataset.start;
        endTime = visibleSubs[0].dataset.end;
      }

      else {
        startTime = visibleSubs[0].dataset.start;
        endTime = visibleSubs[visibleSubs.length - 1].dataset.end;
      }

      if (currentTime > endTime)
        player.seekTo(startTime - 0.100);

    }

    if (!(changeSubsBool))
      return

    // Remove any visible subtitles
    for (let i = 0; i < visibleSubs.length; i++)
      visibleSubs[i].classList.remove('visible');

    currentSubtitle = subtitlesDiv[currentIndex];

    // If any current sub already, unset them to set the new one.
    if (currentSubtitle !== previousCurrentSubtitle){

      if (previousCurrentSubtitle !== null)
        previousCurrentSubtitle.id = '';

      currentSubtitle = subtitlesDiv[currentIndex]
      currentSubtitle.classList.add('visible');
      currentSubtitle.id = 'current';
    }

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

}

function refreshSubtitles(){

  var currentSub = document.getElementById('current');

  // No subtitles to display.
  if (currentSub === null)
    return

  // Remove any visible subtitles.
  __clearVisible(currentSub);

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