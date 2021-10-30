// Input score at init and on input writing!
var inputSubtitles = document.getElementsByClassName("inputSub");

const total = inputSubtitles.length;

var simpleAnswerModeCheckBox = document.getElementById("simpleAnswerModeCheckBox");
simpleAnswerModeCheckBox.addEventListener('input', refreshAnswer);

var scoreInt = document.getElementById('scoreInt');
const scoreTotal = document.getElementById('scoreTotal');

__setScoreStr();

const submitButton = document.getElementById("submitButton");
submitButton.addEventListener('input', submitButton);

function __setScoreStr(){
  scoreInt.innerText = document.getElementsByClassName('correctInput').length;
  scoreTotal.innerText = `/${total}`;
}

function refreshAnswer() {
  for (let i = 0; i < inputSubtitles.length; i++) {
    __validateAnswer(inputSubtitles[i]);
  }

  __setScoreStr();
}

for (let i = 0; i < inputSubtitles.length; i++) {
    inputSubtitles[i].addEventListener('input', validateAnswer);
}

function __toAscii(inStr){
  return inStr.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
}

function __isNonAsciiEqual(a, b) {
  //todo! check : and ? operators!
    return typeof a === 'string' && typeof b === 'string'
        ? a.localeCompare(b, undefined, { sensitivity: 'accent' }) === 0
        : a === b;
}

function __isCorrectAnswer(inStr, inStr2, isSimpleMode){

  if (isSimpleMode)
    return __toAscii(inStr).toUpperCase() === __toAscii(inStr2).toUpperCase()
  else
    return __isNonAsciiEqual(inStr, inStr2)
}

function __validateAnswer(inInputBox){
  correctAnswer = inInputBox.dataset.text;
  isCorrect = false;

  if (simpleAnswerModeCheckBox.checked){
    isCorrect = (__isCorrectAnswer(correctAnswer, inInputBox.value, true));
  }
  else
    isCorrect = (__isCorrectAnswer(correctAnswer, inInputBox.value, false));

  if (isCorrect) {
    inInputBox.classList.add('correctInput')
    inInputBox.classList.remove('incorrectInput')
  }
  else{
    inInputBox.classList.add('incorrectInput')
    inInputBox.classList.remove('correctInput')
  }

}

function validateAnswer(){
  __validateAnswer(this);
}