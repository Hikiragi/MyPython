// Define the variables at the beginning of your script
const questionTypeSelect = document.getElementById('question_type');
const optionsContainer = document.getElementById('options_container');
const shortAnswerContainer = document.getElementById('short_answer_container');
const addOptionBtn = document.getElementById('add_option_btn');
const numOptionsInput = document.getElementById('num_options');
const addQuestionBtn = document.getElementById('add_question_btn');
const explanationLabel = document.querySelector('#options_container label[for="explanation"]');

// Add event listeners after the variables have been defined
questionTypeSelect.addEventListener('change', () => {
  if (questionTypeSelect.value === 'multiple-choice') {
    optionsContainer.style.display = 'block';
    shortAnswerContainer.style.display = 'none';
    addOptionBtn.style.display = 'inline-block';
  } else {
    optionsContainer.style.display = 'none';
    shortAnswerContainer.style.display = 'block';
    addOptionBtn.style.display = 'none';
  }
   document.getElementById('explanation').style.display = 'block';
   explanationLabel.style.display = 'block';
});

addOptionBtn.addEventListener('click', () => {
  const numOptions = parseInt(numOptionsInput.value);
  const newOptionDiv = document.createElement('div');
  newOptionDiv.innerHTML = `
    <input type="radio" name="question_answer" value="${numOptions}">
    <input type="text" name="option_${numOptions}" class="edit-test-specific-option-text">
  `;
  optionsContainer.insertBefore(newOptionDiv, explanationLabel.parentNode);
  numOptionsInput.value = numOptions + 1;
});

addQuestionBtn.addEventListener('click', function() {
  var questionContainer = document.getElementById('new_question_container');
  var newQuestionDiv = document.createElement('div');
  newQuestionDiv.style.margin = '20px 0';

  // Create the question text input
  var questionTextLabel = document.createElement('label');
  questionTextLabel.textContent = 'Вопрос:';
  var questionTextInput = document.createElement('input');
  questionTextInput.type = 'text';
  questionTextInput.name = 'Question Text: ';
  questionTextInput.setAttribute("class", "eidt-specific-test-input")
  newQuestionDiv.appendChild(questionTextLabel);
  newQuestionDiv.appendChild(questionTextInput);
  newQuestionDiv.appendChild(document.createElement('br'));

  // Create the question type select
  var questionTypeLabel = document.createElement('label');
  questionTypeLabel.textContent = 'Тип вопроса: ';
  var questionTypeSelect = document.createElement('select');
  questionTypeSelect.name = 'question_type';
  questionTypeSelect.setAttribute("class", "eidt-specific-test-input")
  var multipleChoiceOption = document.createElement('option');
  multipleChoiceOption.value = 'multiple-choice';
  multipleChoiceOption.textContent = 'Множественный выбор';
  var shortAnswerOption = document.createElement('option');
  shortAnswerOption.value = 'short-answer';
  shortAnswerOption.textContent = 'Вопрос-ответ';
  questionTypeSelect.appendChild(multipleChoiceOption);
  questionTypeSelect.appendChild(shortAnswerOption);
  newQuestionDiv.appendChild(questionTypeLabel);
  newQuestionDiv.appendChild(questionTypeSelect);
  newQuestionDiv.appendChild(document.createElement('br'));

  // Create the options container
  var optionsContainer = document.createElement('div');
  optionsContainer.id = 'options_container';
  var optionsLabel = document.createElement('label');
  optionsLabel.textContent = 'Варианты ответа:';
  optionsContainer.appendChild(optionsLabel);
  // Add two initial options
  for (var i = 0; i < 2; i++) {
    var optionDiv = document.createElement('div');
    var optionInput = document.createElement('input');
    optionInput.type = 'text';
    optionInput.name = 'option_' + i;
    optionInput.setAttribute("class", "edit-test-specific-option-text")
    var correctInput = document.createElement('input');
    correctInput.type = 'radio';
    correctInput.name = 'question_' + questionContainer.querySelectorAll('.question').length + '_answer'; // Use correct name for the radio button
    var correctLabel = document.createElement('label');
//    correctLabel.textContent = 'Correct';
    optionDiv.appendChild(optionInput);
    optionDiv.appendChild(correctInput);
//    optionDiv.appendChild(correctLabel);
    optionsContainer.appendChild(optionDiv);
    optionsContainer.appendChild(document.createElement('br'));
  }
  // Add the "Add Option" button
var addOptionBtn = document.createElement('button');
addOptionBtn.type = 'button';
addOptionBtn.id = 'add_option_btn';
addOptionBtn.textContent = 'Добавить вариант ответа';
addOptionBtn.setAttribute("class", "edit-specific-test-btn")
addOptionBtn.addEventListener('click', function() {
  var numOptions = optionsContainer.querySelectorAll('div').length;
  var optionDiv = document.createElement('div');

  // Create text input for option text
  var optionTextInput = document.createElement('input');
  optionTextInput.type = 'text';
  optionTextInput.className = 'option_text';
  optionTextInput.setAttribute("class", "edit-test-specific-option-text")
  optionTextInput.name = 'option_text_' + numOptions;
  optionDiv.appendChild(optionTextInput);


  // Create radio input for option selection
  var optionRadioInput = document.createElement('input');
  optionRadioInput.type = 'radio';
  optionRadioInput.className = 'option_selection';
  optionRadioInput.name = 'question_' + questionContainer.querySelectorAll('.question').length + '_answer';
  optionDiv.appendChild(optionRadioInput);

  // Create hidden input for option correctness
  var optionHiddenInput = document.createElement('input');
  optionHiddenInput.type = 'hidden';
  optionHiddenInput.className = 'option_correct';
  optionHiddenInput.name = 'option_correct_' + numOptions;
  optionHiddenInput.value = 'false';
  optionDiv.appendChild(optionHiddenInput);



  optionsContainer.appendChild(optionDiv);
  optionsContainer.appendChild(document.createElement('br'));

});

newQuestionDiv.appendChild(optionsContainer);

  // Create the explanation input for multiple-choice questions
  var explanationLabel = document.createElement('label');
  explanationLabel.textContent = 'Пояснение: ';
  var explanationInput = document.createElement('input');
  explanationInput.type = 'text';
  explanationInput.name = 'explanation';
  explanationInput.setAttribute("class", "eidt-specific-test-input")
  newQuestionDiv.appendChild(explanationLabel);
  newQuestionDiv.appendChild(explanationInput);
  newQuestionDiv.appendChild(document.createElement('br'));

  newQuestionDiv.appendChild(addOptionBtn);

  // Create the short answer container
  var shortAnswerContainer = document.createElement('div');
  shortAnswerContainer.id = 'short_answer_container';
  shortAnswerContainer.style.display = 'none';
  var correctAnswerLabel = document.createElement('label');
  correctAnswerLabel.textContent = 'Правильный ответ: ';
  var correctAnswerInput = document.createElement('input');
  correctAnswerInput.type = 'text';
  correctAnswerInput.name = 'correct_answer';
  correctAnswerInput.setAttribute("class", "eidt-specific-test-input")
  shortAnswerContainer.appendChild(correctAnswerLabel);
  shortAnswerContainer.appendChild(correctAnswerInput);
  shortAnswerContainer.appendChild(document.createElement('br'));
  newQuestionDiv.appendChild(shortAnswerContainer);

  // Add a separator line between questions
  questionContainer.appendChild(newQuestionDiv);
  questionContainer.appendChild(document.createElement('hr'));

  // Add an event listener to the question type select to show/hide the short answer container and the explanation input
  questionTypeSelect.addEventListener('change', function() {
    if (this.value === 'short-answer') {
      shortAnswerContainer.style.display = 'block';
      optionsContainer.style.display = 'none';
      addOptionBtn.style.display = 'none';
    } else {
      shortAnswerContainer.style.display = 'none';
      optionsContainer.style.display = 'block';
      addOptionBtn.style.display = 'inline-block';
    }
  });
});

function saveTestData() {
  // Collect the test name and description
  const test_name = document.getElementById('test_name').value;
  const test_description = document.getElementById('test_description').value;

  // Initialize the questions array
  const questions = [];

  // Collect the data for each question
  const question_containers = document.querySelectorAll('.question_container');
  question_containers.forEach((question_container, index) => {
    const question_text = question_container.querySelector('.question_text').value;
    const question_type = question_container.querySelector('.question_type').value;

    // Initialize the options array (for multiple-choice questions) or the correct_answer variable (for short-answer questions)
    const options = [];
    let correct_answer = null;

    if (question_type === 'multiple-choice') {
      // Collect the data for each option in a multiple-choice question
      const option_containers = question_container.querySelectorAll('.option_container');
      option_containers.forEach((option_container) => {
        const option_text = option_container.querySelector('.option_text').value;
        const option_correct = option_container.querySelector('.option_correct').checked;

        options.push({
          'text': option_text,
          'correct': option_correct
        });

        if (option_correct) {
          correct_answer = option_text;
        }
      });
    } else if (question_type === 'short-answer') {
      // Collect the correct answer for a short-answer question
      correct_answer = question_container.querySelector('.question_correct_answer').value;
    }

    // Collect the explanation for the question
    const explanation = question_container.querySelector('.question_explanation').value;

    // Construct the question object and add it to the questions array
    questions.push({
      'text': question_text,
      'type': question_type,
      'options': options,
      'correct_answer': correct_answer,
      'explanation': explanation
    });
  });

  // Construct the test object
  const test_data = {
    'name': test_name,
    'description': test_description,
    'questions': questions
  };

  // Send the test data to the server (you can use fetch, axios, or any other library for that)
  fetch('/save_test_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(test_data)
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response from the server (e.g., show a success message)
    console.log('Success:', data);
  })
  .catch((error) => {
    // Handle the error (e.g., show an error message)
    console.error('Error:', error);
  });
}


document.getElementById('save_changes').addEventListener('click', function() {
  saveTestData();
});
