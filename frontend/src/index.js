let users = [];
let courts = [];
let bookings = [];
<<<<<<< HEAD
const DEFAULT_USER_ID = "nafalza";

// Set minimum date to today
document.getElementById('booking-date').min = new Date().toISOString().split('T')[0];

// Fetch and render courts
function setCourts(data) {
  courts = data;
  renderCourtSelect();
  renderCourts();
}

function renderCourts() {
  const courtsList = document.getElementById('courts-list');
  if (!courts.length) {
    courtsList.innerHTML = '<div class="court-item">No courts available at the moment.</div>';
    return;
  }
  courtsList.innerHTML = courts.map(court => `
    <div class="court-item">
      <h3>${court.name}</h3>
      <p>${court.address || court.location || "Location not specified"}</p>
      <p><strong>Price:</strong> ${formatPrice(court.price_per_hour || 0)}</p>
    </div>
  `).join('');
}

function renderCourtSelect() {
  const select = document.getElementById('booking-court');
  const options = courts.map(c => 
    `<option value="${c.id}">${c.name} (${formatPrice(c.price_per_hour || 0)})</option>`
  );
  select.innerHTML = '<option value="">Select a court</option>' + options.join('');
}

// Fetch and render bookings
function setBookings(data) {
  bookings = data;
  renderBookings();
}

function renderBookings() {
  const bookingsList = document.getElementById('bookings-list');
  if (!bookings.length) {
    bookingsList.innerHTML = '<div class="booking-item">No bookings yet.</div>';
    return;
  }
  bookingsList.innerHTML = bookings.map(booking => {
    const court = courts.find(c => c.id === booking.court_id) || { name: 'Unknown Court' };
    return `
      <div class="booking-item">
        <h3>${court.name}</h3>
        <p><strong>Date:</strong> ${formatDate(booking.time_slot)}</p>
        <p><strong>Status:</strong> <span class="status-${booking.status.toLowerCase()}">${booking.status}</span></p>
      </div>
    `;
  }).join('');
}

// Booking form submission
document.getElementById('booking-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const button = this.querySelector('button');
  const status = document.getElementById('booking-status');
  const courtId = this.querySelector('#booking-court').value;
  const date = this.querySelector('#booking-date').value;

  if (!courtId || !date) {
    showStatus('Please fill in all fields', 'error');
    return;
  }

  button.disabled = true;
  button.textContent = 'Booking...';

=======
let signedInUser = null;

async function fetchAndShow(endpoint, setter, renderFn, elId) {
  const el = document.getElementById(elId);
  try {
    const res = await fetch(endpoint);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    setter(data);
    el.innerHTML = renderFn(data);
  } catch (e) {
    el.innerHTML = `<div class="error">Failed to load: ${e.message}</div>`;
  }
}

// Fetch users and render user list
function setUsers(data) { users = data; }
function renderUsers(data) {
  return `<ul>${data.map(u => `<li><b>${u.name}</b> (${u.email})</li>`).join('')}</ul>`;
}
fetchAndShow('http://localhost:8000/users/', setUsers, renderUsers, 'users-list');

// Fetch courts and render court list and booking select
function setCourts(data) { courts = data; renderCourtSelect(); }
function renderCourts(data) {
  return `<ul>${data.map(c => `<li><b>${c.name}</b> - ${c.location}</li>`).join('')}</ul>`;
}
fetchAndShow('http://localhost:8001/courts/', setCourts, renderCourts, 'courts-list');

// Fetch bookings and render with user/court names
function setBookings(data) { bookings = data; }
function renderBookings(data) {
  return `<ul>${data.map(b => {
    const user = users.find(u => u._id === b.user_id) || { name: b.user_id };
    const court = courts.find(c => c._id === b.court_id) || { name: b.court_id };
    return `<li><b>${user.name}</b> booked <b>${court.name}</b> on <b>${b.date}</b></li>`;
  }).join('')}</ul>`;
}
function refreshBookings() {
  fetchAndShow('http://localhost:8002/bookings/', setBookings, renderBookings, 'bookings-list');
}
refreshBookings();

// Render court select options for booking form
function renderCourtSelect() {
  const select = document.getElementById('booking-court');
  select.innerHTML = courts.map(c => `<option value="${c._id}">${c.name} (${c.location})</option>`).join('');
}

// Sign In logic
document.getElementById('signin-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const email = document.getElementById('signin-email').value;
  const user = users.find(u => u.email === email);
  const status = document.getElementById('signin-status');
  if (user) {
    signedInUser = user;
    status.innerHTML = `<div class="signed-in">Signed in as ${user.name}</div>`;
  } else {
    signedInUser = null;
    status.innerHTML = `<div class="error">User not found</div>`;
  }
});

// Booking form logic
document.getElementById('booking-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const status = document.getElementById('booking-status');
  if (!signedInUser) {
    status.innerHTML = `<div class="error">Please sign in first.</div>`;
    return;
  }
  const courtId = document.getElementById('booking-court').value;
  const date = document.getElementById('booking-date').value;
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4
  try {
    const res = await fetch('http://localhost:8002/bookings/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
<<<<<<< HEAD
      body: JSON.stringify({
        user_id: DEFAULT_USER_ID,
        court_id: courtId,
        time_slot: `${date}T08:00:00Z`,
        duration: 2,
        booking_date: date,
        booking_by: DEFAULT_USER_ID,
        status: "pending",
        payment_status: "unpaid",
        confirmation_code: ""
      })
    });

    if (!res.ok) throw new Error(await res.text());

    showStatus('Booking successful!', 'success');
    this.reset();
    await refreshData();
  } catch (e) {
    showStatus(`Booking failed: ${e.message}`, 'error');
  } finally {
    button.disabled = false;
    button.textContent = 'Book Now';
  }
});

// Helper functions
function showStatus(message, type = 'success') {
  const status = document.getElementById('booking-status');
  status.className = `status ${type}`;
  status.textContent = message;
  setTimeout(() => status.classList.add('hidden'), 5000);
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function formatPrice(price) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR'
  }).format(price);
}

async function fetchData(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
  return await res.json();
}

async function refreshData() {
  try {
    const [courtsData, bookingsData] = await Promise.all([
      fetchData('http://localhost:8001/courts/'),
      fetchData('http://localhost:8002/bookings/')
    ]);
    setCourts(courtsData);
    setBookings(bookingsData);
  } catch (e) {
    console.error('Failed to fetch data:', e);
    showStatus('Failed to load data. Please try again later.', 'error');
  }
}

// Initial load
refreshData();
=======
      body: JSON.stringify({ user_id: signedInUser._id, court_id: courtId, date })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    status.innerHTML = `<div class="signed-in">Booking successful!</div>`;
    refreshBookings();
  } catch (e) {
    status.innerHTML = `<div class="error">Booking failed: ${e.message}</div>`;
  }
});
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4
