const questions = [
    {
        question: "What is HTML?",
        options: ["Programming Language", "Markup Language", "Database", "Operating System"],
        answer: 1
    },
    {
        question: "Which is used for styling?",
        options: ["HTML", "Python", "CSS", "C++"],
        answer: 2
    },
    {
        question: "Which is JavaScript framework?",
        options: ["Django", "React", "Flask", "Laravel"],
        answer: 1
    },
    {
        question: "Which keyword is used for variable?",
        options: ["int", "var", "string", "float"],
        answer: 1
    },
    {
        question: "Which is not programming language?",
        options: ["Java", "Python", "HTML", "C"],
        answer: 2
    }
];

let currentQuestionIndex = 0;
let score = 0;

const questionEl = document.getElementById("question");
const answersEl = document.getElementById("answers");
const nextBtn = document.getElementById("nextBtn");
const resultEl = document.getElementById("result");

function loadQuestion() {
    resetState();
    let currentQuestion = questions[currentQuestionIndex];
    questionEl.innerText = currentQuestion.question;

    currentQuestion.options.forEach((option, index) => {
        const button = document.createElement("button");
        button.innerText = option;
        button.classList.add("btn");
        button.addEventListener("click", () => selectAnswer(button, index));
        answersEl.appendChild(button);
    });
}

function resetState() {
    nextBtn.style.display = "none";
    answersEl.innerHTML = "";
}

function selectAnswer(selectedBtn, selectedIndex) {
    const correctIndex = questions[currentQuestionIndex].answer;
    const buttons = document.querySelectorAll(".btn");

    buttons.forEach((btn, index) => {
        btn.disabled = true;

        if (index === correctIndex) {
            btn.classList.add("correct");
        }
    });

    if (selectedIndex === correctIndex) {
        score++;
    } else {
        selectedBtn.classList.add("wrong");
    }

    nextBtn.style.display = "block";
}

nextBtn.addEventListener("click", () => {
    currentQuestionIndex++;

    if (currentQuestionIndex < questions.length) {
        loadQuestion();
    } else {
        showResult();
    }
});

function showResult() {
    questionEl.style.display = "none";
    answersEl.style.display = "none";
    nextBtn.style.display = "none";

    resultEl.innerText = `You scored ${score} out of ${questions.length}`;

    const restartBtn = document.createElement("button");
    restartBtn.innerText = "Restart";
    restartBtn.classList.add("btn");
    restartBtn.onclick = () => location.reload();

    resultEl.appendChild(document.createElement("br"));
    resultEl.appendChild(restartBtn);
}

// Start Quiz
loadQuestion();