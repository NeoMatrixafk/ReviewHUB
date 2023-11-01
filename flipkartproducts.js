let clickInProgress = false;
async function fetchJsonFile() {
    try {
        const response = await fetch('flipkartproducts.json');
        const jsonData = await response.json();

        processJsonData(jsonData);
    } catch (error) {
        console.error('Error loading JSON file:', error);
    }
}

    function processJsonData(jsonData) {
        console.log(jsonData);
        const container = document.getElementById('product-container');

        jsonData.slice(0, 24).forEach((product, index) => {
            const box = document.createElement('div');
            box.className = 'box';

            const image = document.createElement('img');
            image.className = 'product-image';
            image.src = product['Image Link'];
            image.alt = 'Product ' + (index + 1);

            const name = document.createElement('p');
            name.className = 'product-name';
            name.textContent = product['Product Name'];

            const productLink = product['Product Link'];
            box.setAttribute('data-product-link', productLink);

            box.appendChild(image);
            box.appendChild(name);

            container.appendChild(box);

            box.addEventListener('click', function () {
            if (!clickInProgress) {
                clickInProgress = true;
                const productLink = this.getAttribute('data-product-link');
                if (productLink) {
                    saveProductLinkToFile(productLink)
                        .finally(() => {
                            clickInProgress = false;
                        });
                }
            }
        });
    });
}

    function saveProductLinkToFile(productLink) {

    fetch('http://localhost:5000/flipkart_save_product_link', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ productLink }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.message === 'Product Link saved successfully') {
            console.log('Product Link saved successfully.');
        } else {
            console.error('Failed to save Product Link:', data.message);
        }
    })
    .catch((error) => {
        console.error('Error saving Product Link:', error);
    });
}

fetchJsonFile();
