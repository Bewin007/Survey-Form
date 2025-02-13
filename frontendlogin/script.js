// script.js
function addQuestion(type) {
  const container = document.getElementById('survey-container');
  let questionHTML = '';

  if (type === 'multiple-choice') {
    questionHTML = `
      <div class="question">
        <input type="text" placeholder="Enter your question">
        <div>
          <input type="text" placeholder="Option 1">
          <input type="text" placeholder="Option 2">
        </div>
      </div>
    `;
  } else if (type === 'text') {
    questionHTML = `
      <div class="question">
        <input type="text" placeholder="Enter your question">
        <input type="text" placeholder="Text input">
      </div>
    `;
  } else if (type === 'rating') {
    questionHTML = `
      <div class="question">
        <input type="text" placeholder="Enter your question">
        <input type="range" min="1" max="5">
      </div>
    `;
  }

  container.insertAdjacentHTML('beforeend', questionHTML);
}