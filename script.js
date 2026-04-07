const container = document.getElementById("products");

// 🔴 CHANGE THIS TO YOUR BACKEND URL
const API_URL = "https://your-replit-url/products";

fetch(API_URL)
  .then(res => res.json())
  .then(products => {
    products.forEach(p => {
      const div = document.createElement("div");
      div.className = "item";

      let opts = "";
      p.options.forEach(o => {
        opts += `<option value="${o}">${o}</option>`;
      });

      div.innerHTML = `
        <h3>${p.name}</h3>
        <p>$${p.price}</p>
        <select id="opt-${p.id}">
          ${opts}
        </select>
        <button onclick="buy(${p.id}, '${p.name}', ${p.price})">Buy</button>
      `;

      container.appendChild(div);
    });
  });

function buy(id, name, price) {
  const option = document.getElementById(`opt-${id}`).value;

  Telegram.WebApp.sendData(JSON.stringify({
    id, name, option, price
  }));
}
