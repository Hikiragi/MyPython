function moveFiles() {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:5000/moving_files', true);
  xhr.send();
}

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector("button[type='submit']").addEventListener('click', function(event) {
    event.preventDefault();

    var name = document.querySelector("#test-name").value;
    var description = document.querySelector("#test-description").value;
    var questions = [];
    var questionIndex = 0;
    document.querySelectorAll(".question-block").forEach(function(block) {
      var questionType = block.querySelector("select[name='question-type']").value;
      var questionText = block.querySelector(".question-text").value;
      var index = "question_" + questionIndex + "_question";
      questionIndex++;

      if (questionType === 'multiple-choice') {
        var options = [];
        block.querySelectorAll(".option-text").forEach(function(option, index) {
          var correct = false;
          if (block.querySelector(`input[name='correct-option'][value='${index}']`).checked) {
            correct = true;
          }
          options.push({ text: option.value, correct: correct });
        });
        var correctAnswer = options.find(option => option.correct).text;
        var explanation = block.querySelector(".explanation").value; // Add explanation for multiple-choice questions
        questions.push({ text: questionText, type: questionType, options: options, correct_answer: correctAnswer, explanation: explanation });
      } else if (questionType === 'short-answer') {
        var correctAnswer = block.querySelector(".correct-answer").value;
        var explanation = block.querySelector(".explanation").value; // Add explanation for short-answer questions
        questions.push({ text: questionText, type: questionType, correct_answer: correctAnswer, explanation: explanation });
      }

    });

    var data = JSON.stringify({ name: name, description: description, questions: questions }, null, 2);
    var blob = new Blob([data], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", name + ".json");
    document.body.appendChild(link);
    link.click();
    setTimeout(function() {
      link.remove();
      URL.revokeObjectURL(url);
    }, 100);
  });

  document.querySelector("#add-question-btn").addEventListener('click', function() {
    var questionBlock = document.createElement("div");
questionBlock.classList.add("question-block");
questionBlock.style.marginBottom = "20px"; // добавлена эта строчка

var questionTypeLabel = document.createElement("label");
questionTypeLabel.textContent = "Тип вопроса:";
questionBlock.appendChild(questionTypeLabel);

var questionTypeSelect = document.createElement("select");
questionTypeSelect.setAttribute("name", "question-type");
questionTypeSelect.setAttribute("class", "create-test-question-selector")
questionBlock.appendChild(questionTypeSelect);

var questionTypeOptionMultiple = document.createElement("option");
questionTypeOptionMultiple.setAttribute("value", "multiple-choice");
questionTypeOptionMultiple.textContent = "Множественный выбор";
questionTypeSelect.appendChild(questionTypeOptionMultiple);

var questionTypeOptionShort = document.createElement("option");
questionTypeOptionShort.setAttribute("value", "short-answer");
questionTypeOptionShort.textContent = "Вопрос-ответ";
questionTypeSelect.appendChild(questionTypeOptionShort);

var questionLabel = document.createElement("label");
questionBlock.appendChild(document.createElement("br"))
questionLabel.textContent = "Вопрос: ";
questionBlock.appendChild(questionLabel);

var questionText = document.createElement("input");
questionText.setAttribute("type", "text");
questionText.setAttribute("class", "create-test-question-text")
questionText.classList.add("question-text");
questionBlock.appendChild(questionText);

// Add explanation input for multiple-choice questions
var explanationContainer = document.createElement("div"); // создан новый элемент div

var explanationLabel = document.createElement("label");
explanationLabel.textContent = "Пояснение:";
explanationContainer.appendChild(explanationLabel); // добавлен элемент explanationLabel в элемент explanationContainer

var explanationInput = document.createElement("input");
explanationInput.setAttribute("type", "text");
explanationInput.setAttribute("class", "create-test-question-text");
explanationInput.classList.add("explanation");
explanationContainer.appendChild(explanationInput); // добавлен элемент explanationInput в элемент explanationContainer

questionBlock.appendChild(explanationContainer); // добавлен элемент explanationContainer в элемент questionBlock после элемента questionText


var optionsContainer = document.createElement("div");
for (var i = 0; i < 1; i++) {
  var optionContainer = document.createElement("div");

  var optionText = document.createElement("input");
  optionText.setAttribute("type", "text");
  optionText.setAttribute("class", "create-test-question-text");
  optionText.classList.add("option-text");
  optionContainer.appendChild(optionText);

  var correctOptionRadio = document.createElement("input");
  correctOptionRadio.setAttribute("type", "radio");
  correctOptionRadio.setAttribute("name", "correct-option");
  correctOptionRadio.setAttribute("class", "create-test-radio-option")
  correctOptionRadio.setAttribute("value", i);
  optionContainer.appendChild(correctOptionRadio);

  optionsContainer.appendChild(optionContainer);
}
questionBlock.appendChild(optionsContainer);


var addOptionButton = document.createElement("button");
addOptionButton.setAttribute("type", "button");
addOptionButton.setAttribute("class", "add-question-btn-create-test")
addOptionButton.textContent = "Добавить вариант";
addOptionButton.addEventListener("click", function() {
  var optionContainer = document.createElement("div");

  var optionText = document.createElement("input");
  optionText.setAttribute("type", "text");
  optionText.setAttribute("class", "create-test-question-text");
  optionText.classList.add("option-text");
  optionContainer.appendChild(optionText);

  var correctOptionRadio = document.createElement("input");
  correctOptionRadio.setAttribute("type", "radio");
  correctOptionRadio.setAttribute("name", "correct-option");
  correctOptionRadio.setAttribute("class", "create-test-radio-option")
  correctOptionRadio.setAttribute("value", optionsContainer.children.length);
  optionContainer.appendChild(correctOptionRadio);

  optionsContainer.appendChild(optionContainer);
});
questionBlock.appendChild(addOptionButton);

var shortAnswerContainer = document.createElement("div");
shortAnswerContainer.style.display = "none";

var correctAnswerLabel = document.createElement("label");
correctAnswerLabel.textContent = "Правильный ответ:";
shortAnswerContainer.appendChild(correctAnswerLabel);

var correctAnswer = document.createElement("input");
correctAnswer.setAttribute("type", "text");
correctAnswer.setAttribute("class", "create-test-question-text")
correctAnswer.classList.add("correct-answer");
shortAnswerContainer.appendChild(correctAnswer);

// удалены строчки, которые создают поле ввода explanation для коротких ответов

questionBlock.appendChild(shortAnswerContainer);

questionTypeSelect.addEventListener("change", function() {
  if (this.value === "short-answer") {
    optionsContainer.style.display = "none";
    addOptionButton.style.display = "none";
    shortAnswerContainer.style.display = "block";
  } else {
    optionsContainer.style.display = "block";
    addOptionButton.style.display = "block";
    shortAnswerContainer.style.display = "none";
  }
});

var removeButton = document.createElement("button");
removeButton.textContent = "Удалить вопрос";
removeButton.setAttribute("class", "add-question-btn-create-test")
removeButton.addEventListener("click", function() {
  questionBlock.remove();
});
questionBlock.appendChild(removeButton);

document.querySelector(".question-container").appendChild(questionBlock);



  });
  document.querySelector("#create-test-btn").addEventListener('click', function(event) {
    event.preventDefault();

    // Existing code for creating a new test

    window.location.href = '/move_files';
  });
});
