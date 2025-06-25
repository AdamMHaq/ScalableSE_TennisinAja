// API Configuration
const API_BASE_URL = 'http://localhost';
const USER_SERVICE_URL = `${API_BASE_URL}:8000`;
const COURT_SERVICE_URL = `${API_BASE_URL}:8001`;
const BOOKING_SERVICE_URL = `${API_BASE_URL}:8002`;

let users = [];
let courts = [];
let bookings = [];
let signedInUser = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, initializing app...');
  
  // Set minimum date to today
  const dateInput = document.getElementById('booking-date');
  if (dateInput) {
    dateInput.min = new Date().toISOString().split('T')[0];
  }
  
  // Load initial data
  loadInitialData();
  setupEventListeners();
});

// Load initial data
async function loadInitialData() {
  console.log('Loading initial data...');
  await fetchCourts();
  await fetchBookings();
}

// Setup event listeners
function setupEventListeners() {
  const bookingForm = document.getElementById('booking-form');
  if (bookingForm) {
    bookingForm.addEventListener('submit', handleBookingSubmit);
  }
}

// Fetch and display courts
async function fetchCourts() {
  console.log('Fetching courts...');
  try {
    const response = await fetch(`${COURT_SERVICE_URL}/courts/public`);
    console.log('Court API response status:', response.status);
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    console.log('Courts data:', data);
    
    setCourts(data);
  } catch (error) {
    console.error('Failed to fetch courts:', error);
    const courtsList = document.getElementById('courts-list');
    if (courtsList) {
      courtsList.innerHTML = `<div class="court-item">Failed to load courts: ${error.message}</div>`;
    }
  }
}

function setCourts(data) {
  console.log('Setting courts:', data);
  courts = data;
  renderCourtSelect();
  renderCourts();
}

function renderCourts() {
  console.log('Rendering courts, count:', courts.length);
  const courtsList = document.getElementById('courts-list');
  if (!courtsList) {
    console.error('Courts list element not found');
    return;
  }
  
  if (!courts.length) {
    courtsList.innerHTML = '<div class="court-item">No courts available at the moment.</div>';
    return;
  }
  
  courtsList.innerHTML = courts.map(court => `
    <div class="court-item">
      <h3>${court.name}</h3>
      <p><strong>📍 Location:</strong> ${court.address}</p>
      <p><strong>💵 Price:</strong> ${formatPrice(court.price_per_hour)}</p>
      <p><strong>🏟️ Surface:</strong> ${court.surface}</p>
      <p><strong>🏠 Type:</strong> ${court.is_indoor ? 'Indoor' : 'Outdoor'}</p>
      <p><strong>📞 Contact:</strong> ${court.contact_phone}</p>
      <p><strong>🎾 Available Courts:</strong> ${court.available_courts}</p>
      <a href="${court.gmaps_link}" target="_blank" style="color: #2b5876;">📍 View on Maps</a>
    </div>
  `).join('');
  
  console.log('Courts rendered successfully');
}

function renderCourtSelect() {
  const select = document.getElementById('booking-court');
  if (!select) return;
  
  const options = courts.map(c => 
    `<option value="${c.id}">${c.name} (${formatPrice(c.price_per_hour)})</option>`
  );
  select.innerHTML = '<option value="">Select a court</option>' + options.join('');
}

// Fetch and display bookings
async function fetchBookings() {
  console.log('Fetching bookings...');
  try {
    const response = await fetch(`${BOOKING_SERVICE_URL}/bookings/`);
    console.log('Booking API response status:', response.status);
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    console.log('Bookings data:', data);
    
    setBookings(data);
  } catch (error) {
    console.error('Failed to fetch bookings:', error);
    const bookingsList = document.getElementById('bookings-list');
    if (bookingsList) {
      bookingsList.innerHTML = `<div class="booking-item">Failed to load bookings: ${error.message}</div>`;
    }
  }
}

function setBookings(data) {
  bookings = data;
  renderBookings();
}

function renderBookings() {
  const bookingsList = document.getElementById('bookings-list');
  if (!bookingsList) return;
  
  if (!bookings.length) {
    bookingsList.innerHTML = '<div class="booking-item">No bookings yet.</div>';
    return;
  }
  
  bookingsList.innerHTML = bookings.map(booking => {
    const court = courts.find(c => c.id === booking.court_id) || { name: 'Unknown Court' };
    return `
      <div class="booking-item">
        <h3>${court.name}</h3>
        <p><strong>Date:</strong> ${formatDate(booking.booking_date)}</p>
        <p><strong>Time:</strong> ${booking.time_slot}</p>
        <p><strong>Duration:</strong> ${booking.duration} hour(s)</p>
        <p><strong>Status:</strong> <span class="status-${booking.status.toLowerCase()}">${booking.status}</span></p>
        <p><strong>Payment:</strong> <span class="status-${booking.payment_status.toLowerCase()}">${booking.payment_status}</span></p>
        ${booking.confirmation_code ? `<p><strong>Code:</strong> ${booking.confirmation_code}</p>` : ''}
      </div>
    `;
  }).join('');
}

// Handle booking form submission
async function handleBookingSubmit(e) {
  e.preventDefault();
  const button = e.target.querySelector('button');
  const courtId = e.target.querySelector('#booking-court').value;
  const date = e.target.querySelector('#booking-date').value;

  if (!courtId || !date) {
    showStatus('Please fill in all fields', 'error');
    return;
  }

  button.disabled = true;
  button.textContent = 'Booking...';

  try {
    const bookingData = {
      user_id: "demo_user",
      court_id: courtId,
      time_slot: "09:00",
      duration: 2,
      booking_date: new Date(date).toISOString(),
      booking_by: "demo_user",
      status: "pending",
      payment_status: "unpaid",
      confirmation_code: generateConfirmationCode()
    };

    const response = await fetch(`${BOOKING_SERVICE_URL}/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingData)
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    
    showStatus('Booking created successfully!', 'success');
    e.target.reset();
    await fetchBookings(); // Refresh bookings list
    
  } catch (error) {
    showStatus(`Failed to create booking: ${error.message}`, 'error');
  } finally {
    button.disabled = false;
    button.textContent = 'Book Now';
  }
}

// Utility functions
function formatPrice(price) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(price);
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

function showStatus(message, type) {
  const status = document.getElementById('booking-status');
  if (status) {
    status.innerHTML = `<div class="status ${type}">${message}</div>`;
    setTimeout(() => {
      status.innerHTML = '';
    }, 5000);
  }
}

function generateConfirmationCode() {
  return Math.random().toString(36).substr(2, 8).toUpperCase();
}
