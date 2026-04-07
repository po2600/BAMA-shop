const products = [
  {
    id: 1,
    name: "Tank Top",
    price: 10,
    options: ["Black", "White"]
  }
];

const container = document.getElementById("products");

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
    <button onclick="buy(${p.id})">Buy</button>
  `;

  container.appendChild(div);
});

function buy(id) {
  const product = products.find(p => p.id === id);
  const option = document.getElementById(`opt-${id}`).value;

  Telegram.WebApp.sendData(JSON.stringify({
    id: id,
    name: product.name,
    option: option,
    price: product.price
  }));
}
