javascript
const tg = window.Telegram.WebApp;
tg.expand(); // Full screen mode

const products = [
    { id: 1, name: "BAMA T-Shirt", price: 10, img: "images/tshirt.jpg" },
    { id: 2, name: "BAMA Hoodie", price: 25, img: "images/hoodie.jpg" },
    { id: 3, name: "BAMA Cap", price: 15, img: "images/cap.jpg" }
];

let cart = [];

// 1. Render Products
const grid = document.getElementById('product-grid');
products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
        <img src="${product.img}" alt="${product.name}">
        <h3>${product.name}</h3>
        <p class="price">$${product.price}</p>
        <button onclick="addToCart(${product.id})">Add to Cart</button>
    `;
    grid.appendChild(card);
});

// 2. Cart Logic
function addToCart(id) {
    const item = products.find(p => p.id === id);
    cart.push(item);
    updateMainButton();
}

function updateMainButton() {
    if (cart.length > 0) {
        const total = cart.reduce((sum, item) => sum + item.price, 0);
        tg.MainButton.text = `VIEW ORDER ($${total})`;
        tg.MainButton.show();
    } else {
        tg.MainButton.hide();
    }
}

// 3. Send Order to Bot
tg.MainButton.onClick(() => {
    const orderDetails = cart.map(i => i.name).join(', ');
    tg.sendData(`Order: ${orderDetails}`); // Sends data and closes app
});
