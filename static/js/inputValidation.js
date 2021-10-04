var inputSubtitles = document.getElementsByClassName("inputSub");

for (let i = 0; i < inputSubtitles.length; i++) {
    inputSubtitles[i].addEventListener('input', validateAnswer);
}

function validateAnswer(){
  correctAsnwer = this.dataset.text
  if (correctAsnwer.startsWith(this.value)) {
    this.classList.add('correctInput')
    this.classList.remove('incorrectInput')
  }
  else{
    this.classList.add('incorrectInput')
    this.classList.remove('correctInput')
  }

}