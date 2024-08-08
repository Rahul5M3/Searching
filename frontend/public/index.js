const searchButton = document.querySelector('.search-button');
const searchField = document.getElementById('search-field');

searchButton.addEventListener('click', () => {
  searchField.style.display = 'block';
});