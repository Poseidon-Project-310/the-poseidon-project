let deliveriesCache = {};

function renderDeliveryPage() {
  const root = document.getElementById("app-root");

  root.innerHTML = `
    <div class="page-card">
      <h2>🚚 Delivery Dashboard</h2>

      <div class="section">
        <h3>Create Delivery</h3>

        <input id="delivery_id" placeholder="Delivery ID" type="number" />
        <input id="order_id" placeholder="Order ID" type="number" />
        <input id="eta" placeholder="ETA (optional)" />
        <input id="driver_name" placeholder="Driver name (optional)" />
        <input id="driver_contact" placeholder="Driver contact (optional)" />

        <select id="status">
          <option value="pending">pending</option>
          <option value="assigned">assigned</option>
          <option value="picked_up">picked_up</option>
          <option value="on_the_way">on_the_way</option>
          <option value="delivered">delivered</option>
        </select>

        <button onclick="createDelivery()">Create</button>
        <div id="create-msg"></div>
      </div>

      <div class="section">
        <h3>All Deliveries</h3>
        <button onclick="loadDeliveries()">Refresh</button>
        <div id="delivery-list"></div>
      </div>
    </div>
  `;

  loadDeliveries();
}

function showMsg(el, text) {
  el.innerText = text;
}

function formatError(detail) {
  if (!detail) return "Error";

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map(item => {
        if (typeof item === "string") return item;
        if (item?.msg) return item.msg;
        return JSON.stringify(item);
      })
      .join(", ");
  }

  if (typeof detail === "object") {
    if (detail.msg) return detail.msg;
    return JSON.stringify(detail);
  }

  return String(detail);
}

async function createDelivery() {
  const msg = document.getElementById("create-msg");

  const delivery_id = parseInt(document.getElementById("delivery_id").value);
  const order_id = parseInt(document.getElementById("order_id").value);
  const status = document.getElementById("status").value;
  const eta = document.getElementById("eta").value.trim();
  const driver_name = document.getElementById("driver_name").value.trim();
  const driver_contact = document.getElementById("driver_contact").value.trim();

  if (!delivery_id || delivery_id <= 0) {
    showMsg(msg, "Invalid delivery ID");
    return;
  }

  if (!order_id || order_id <= 0) {
    showMsg(msg, "Invalid order ID");
    return;
  }

  const payload = {
    delivery_id,
    order_id,
    status,
    estimated_arrival: eta || null,
    driver_name: driver_name || null,
    driver_contact: driver_contact || null
  };

  try {
    const res = await fetch(`${API_BASE}/deliveries/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      showMsg(msg, formatError(data.detail));
      return;
    }

    showMsg(msg, "Created!");

    document.getElementById("delivery_id").value = "";
    document.getElementById("order_id").value = "";
    document.getElementById("eta").value = "";
    document.getElementById("driver_name").value = "";
    document.getElementById("driver_contact").value = "";
    document.getElementById("status").value = "pending";

    loadDeliveries();
  } catch (err) {
    console.error(err);
    showMsg(msg, "Server error");
  }
}

async function loadDeliveries() {
  const container = document.getElementById("delivery-list");
  container.innerHTML = "Loading...";

  try {
    const res = await fetch(`${API_BASE}/deliveries/`);
    const data = await res.json();

    console.log("deliveries response:", data);

    if (!res.ok) {
      container.innerHTML = formatError(data.detail);
      return;
    }

    if (!Array.isArray(data)) {
      container.innerHTML = "Unexpected response format from backend.";
      return;
    }

    if (data.length === 0) {
      deliveriesCache = {};
      container.innerHTML = "No deliveries found.";
      return;
    }

    deliveriesCache = {};
    data.forEach(d => {
      deliveriesCache[d.delivery_id] = d;
    });

    container.innerHTML = data.map(d => `
      <div class="delivery-card">
        <p><b>Delivery ID:</b> ${d.delivery_id ?? "N/A"}</p>
        <p><b>Order ID:</b> ${d.order_id ?? "N/A"}</p>
        <p><b>Status:</b> ${d.status ?? "N/A"}</p>
        <p><b>ETA:</b> ${d.estimated_arrival || "N/A"}</p>
        <p><b>Driver Name:</b> ${d.driver_name || "N/A"}</p>
        <p><b>Driver Contact:</b> ${d.driver_contact || "N/A"}</p>

        <select id="status-${d.delivery_id}">
          <option value="pending" ${d.status === "pending" ? "selected" : ""}>pending</option>
          <option value="assigned" ${d.status === "assigned" ? "selected" : ""}>assigned</option>
          <option value="picked_up" ${d.status === "picked_up" ? "selected" : ""}>picked_up</option>
          <option value="on_the_way" ${d.status === "on_the_way" ? "selected" : ""}>on_the_way</option>
          <option value="delivered" ${d.status === "delivered" ? "selected" : ""}>delivered</option>
        </select>

        <button onclick="updateStatus(${d.delivery_id})">Update</button>
        <button onclick="deleteDelivery(${d.delivery_id})">Delete</button>
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
    container.innerHTML = "Server error";
  }
}

async function updateStatus(id) {
  const existing = deliveriesCache[id];

  if (!existing) {
    alert("Delivery not found");
    return;
  }

  const status = document.getElementById(`status-${id}`).value;

  try {
    const res = await fetch(`${API_BASE}/deliveries/${id}/status`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        status,
        estimated_arrival: existing.estimated_arrival
      })
    });

    const data = await res.json();

    if (!res.ok) {
      alert(formatError(data.detail));
      return;
    }

    loadDeliveries();
  } catch (err) {
    console.error(err);
    alert("Error updating");
  }
}

async function deleteDelivery(id) {
  try {
    const res = await fetch(`${API_BASE}/deliveries/${id}`, {
      method: "DELETE"
    });

    let data = {};
    try {
      data = await res.json();
    } catch {
      data = {};
    }

    if (!res.ok) {
      alert(formatError(data.detail));
      return;
    }

    loadDeliveries();
  } catch (err) {
    console.error(err);
    alert("Error deleting");
  }
}