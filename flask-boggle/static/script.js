//Selecten sections of the html to utilize further in the code
const $guessInput = $("#guess")
const $guessForm = $("#guessForm")
const $board = $("#board")
const $wordList = $("#correctWords")
const $score = $("#score")
const $message = $("#message")
const $timer = $("#timer")
const wordsUsed = []
//Event listener for submitting guesses
$guessForm.on("submit", async function (e){
    e.preventDefault();
    //Check on the server if the word is valid or not
    const val = $guessInput.val();
    const response = await axios.get("/check/"+val);
    const result = response.data.result
    //Response according if the word is valid in the game or not
    if (result === "not-word") {
        showMessage(`The word ${val} is invalid`, "Error")
    } else if(result === "not-on-board"){
        showMessage(`The word ${val} is not on the board`, "Error")
    }else if (wordsUsed.includes(val)){
        showMessage(`The word ${val} has already been used`, "Error")
    }else{
        $wordList.append(`<li>${val}</li>`)
        wordsUsed.push(val)
        updateScore()
    }
    $guessInput.val("");
})

//Displays if the guess is invalid and when the game is done
function showMessage(msg, cls) {
    $("#message")
      .text(msg)
      .removeClass()
      .addClass(`msg ${cls}`);
  }

//Updates the score and displays the new value
function updateScore() {
    scoreInt = parseInt($score.text());
    newScore = scoreInt + $guessInput.val().length;
    $score
      .text(newScore)
}

//Timer for the game
//When the time ends, the input form is removed
const timer = setInterval(async function(){
    startTime = parseInt($timer.text());
    if (startTime < 1){
        clearInterval(timer);
        $timer.text("Time's Out");
        $guessForm.remove()
        await scoreGame();
    }else{
        timeNow = startTime - 1;
        $timer.text(timeNow);
    }
},1000)

//Send the final score to the server and checks if the score is the new Highscore
//Display message according to the servers response
async function scoreGame() {
    const finalScore = parseInt($score.text());
    console.log(finalScore);
    let data = JSON.stringify({ score: finalScore });
    const res = await axios({
        method: 'post',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        url: '/score',
        data: data
      });
    if (res.data.brokeRecord) {
      showMessage(`New record: ${finalScore}`, "ok");
    } else {
      showMessage(`Final score: ${finalScore}`, "ok");
    }
}

