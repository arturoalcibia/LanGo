// Query all subs
var subtitlesDiv = document.getElementsByClassName('sub');

// Get settings
var beforeSettingsInput = document.getElementById("beforeSettingsInput");
beforeSettingsInput.value = 1
var afterSettingsInput  = document.getElementById("afterSettingsInput");
afterSettingsInput.value = 1

// Add all eventListener to input
for (let i = 0; i < subtitlesDiv.length; i++) {
  subtitleDiv = subtitlesDiv[i];
  inputChildren = subtitleDiv.getElementsByClassName('inputSub');

  /*
  //todo! this doesnt werk
  for (let j = 0; j < inputChildren.length; j++) {
     inputChildren[j].addEventListener('input', logValue);
  }
   */
}

function displaySubtitles(){
  currentTime = player.getCurrentTime();
  var indicesToVisible   = []

  for (let i = 0; i < subtitlesDiv.length; i++) {

    subtitleDiv = subtitlesDiv[i]

    //todo! Maybe check if class is already on the list?
    if (currentTime >= subtitleDiv.dataset.start && currentTime <= subtitleDiv.dataset.end) {
      indicesToVisible.push(i);

      for (let j = 1; j < (parseInt(beforeSettingsInput.value) + 1); j++) {

        newIndexBefore = i - j;

        if (newIndexBefore < 1)
          continue

        indicesToVisible.push(newIndexBefore);
      }

      for (let k = 0; k < parseInt(afterSettingsInput.value) + 1; k++) {

        newIndexAfter = k + i;

        if (newIndexAfter >= subtitlesDiv.length )
          continue

        indicesToVisible.push(newIndexAfter);
      }

    }

  }

  if (indicesToVisible.length !== 0){

  var visibleSubs = document.getElementsByClassName('visible');

  for (let i = 0; i < visibleSubs.length; i++)
    visibleSubs[i].classList.remove('visible');

  for (let i = 0; i < indicesToVisible.length; i++)
    subtitlesDiv[indicesToVisible[i]].classList.add('visible');

  }

}