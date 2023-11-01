async function fetchJsonFile() {
    try {
        const response = await fetch('flipkartData.json');
        const jsonData = await response.json();

        processJsonData(jsonData);
    } catch (error) {
        console.error('Error loading JSON file:', error);
    }
}

function processJsonData(jsonData) {
    const container = document.getElementById('product-container');

    jsonData.forEach((review, index) => {
        const box = document.createElement('div');
        box.className = 'box';

        // Create elements for user, title, date, and review content
        const userElement = document.createElement('p');
        userElement.className = 'product-name';
        userElement.textContent = 'User: ' + review.user;

        const titleElement = document.createElement('p');
        titleElement.className = 'product-name';
        titleElement.textContent = 'Title: ' + review.title;

        const dateElement = document.createElement('p');
        dateElement.className = 'product-name';
        dateElement.textContent = 'Date: ' + review.date;

        const reviewContentElement = document.createElement('p');
        reviewContentElement.className = 'product-name';
        reviewContentElement.textContent = 'Review: ' + review.review;

        box.appendChild(userElement);
        box.appendChild(titleElement);
        box.appendChild(dateElement);
        box.appendChild(reviewContentElement);

        container.appendChild(box);
    });
}

fetchJsonFile();
