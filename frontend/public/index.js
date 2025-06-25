// API Configuration
const API_BASE_URL = 'http://localhost';
const USER_SERVICE_URL = `${API_BASE_URL}:8000`;
const COURT_SERVICE_URL = `${API_BASE_URL}:8001`;
const BOOKING_SERVICE_URL = `${API_BASE_URL}:8002`;

// Global state
let users = [];
let courts = [];
let bookings = [];
let currentUser = null;
let authToken = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  console.log('TennisinAja app initializing...');
  
  // Set minimum date to today
  const dateInput = document.getElementById('booking-date');
  if (dateInput) {
    dateInput.min = new Date().toISOString().split('T')[0];
  }
  
  // Check for existing auth token
  checkAuthStatus();
  
  // Load initial data
  loadInitialData();
  setupEventListeners();
});

// Authentication Management
function checkAuthStatus() {
  authToken = localStorage.getItem('tennis_auth_token');
  if (authToken) {
    // Verify token and get user info
    verifyToken();
  } else {
    showAuthCard();
  }
}

async function verifyToken() {
  try {
    const response = await fetch(`${USER_SERVICE_URL}/users/me`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    if (response.ok) {
      currentUser = await response.json();
      showLoggedInState();
    } else {
      // Token is invalid
      logout();
    }
  } catch (error) {
    console.error('Token verification failed:', error);
    logout();
  }
}

function showAuthCard() {
  document.getElementById('auth-card').classList.remove('hidden');
  document.getElementById('booking-card').classList.add('hidden');
  document.getElementById('user-display').textContent = '';
  document.getElementById('logout-btn').classList.add('hidden');
}

function showLoggedInState() {
  document.getElementById('auth-card').classList.add('hidden');
  document.getElementById('booking-card').classList.remove('hidden');
  document.getElementById('user-display').textContent = `Welcome, ${currentUser.name}`;
  document.getElementById('logout-btn').classList.remove('hidden');
  
  // Show/hide admin court addition card
  if (currentUser && currentUser.role === "admin") {
    document.getElementById('add-court-card').style.display = '';
  } else {
    document.getElementById('add-court-card').style.display = 'none';
  }
  
  // Load user-specific data
  fetchBookings();
}

function logout() {
  localStorage.removeItem('tennis_auth_token');
  authToken = null;
  currentUser = null;
  showAuthCard();
  
  // Clear bookings
  document.getElementById('bookings-list').innerHTML = '<div class="booking-item">Please login to view your bookings.</div>';
}

// Tab switching
function switchTab(tabName) {
  // Update tab buttons
  document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
  
  // Find and activate the correct tab button
  const buttons = document.querySelectorAll('.tab-button');
  buttons.forEach(btn => {
    if ((tabName === 'login' && btn.textContent === 'Login') || 
        (tabName === 'register' && btn.textContent === 'Register')) {
      btn.classList.add('active');
    }
  });
  
  // Show/hide tab content
  document.getElementById('login-tab').classList.toggle('hidden', tabName !== 'login');
  document.getElementById('register-tab').classList.toggle('hidden', tabName !== 'register');
}

// Setup event listeners
function setupEventListeners() {
  // Login form
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }
  
  // Register form
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', handleRegister);
  }
  
  // Booking form
  const bookingForm = document.getElementById('booking-form');
  if (bookingForm) {
    bookingForm.addEventListener('submit', handleBookingSubmit);
  }
  
  // Court addition form
  document.getElementById('add-court-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const status = document.getElementById('add-court-status');
    const button = e.target.querySelector('button');
    button.disabled = true;
    button.textContent = 'Adding...';

    const name = document.getElementById('court-name').value;
    const contact_phone = document.getElementById('court-phone').value;
    const address = document.getElementById('court-address').value;
    const gmaps_link = document.getElementById('court-gmaps').value;
    const surface = document.getElementById('court-surface').value;
    const is_indoor = document.getElementById('court-indoor').value === "true";
    const price_per_hour = parseFloat(document.getElementById('court-price').value);
    const available_days = document.getElementById('court-days').value.split(',').map(s => s.trim());
    const available_courts = parseInt(document.getElementById('court-count').value);

    try {
      const response = await fetch(`${COURT_SERVICE_URL}/courts/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
          name, contact_phone, address, gmaps_link, surface, is_indoor,
          price_per_hour, available_days, available_courts
        })
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to add court');
      }
      status.textContent = 'Court added successfully!';
      status.className = 'success';
      e.target.reset();
      await fetchCourts(); // Refresh courts list
    } catch (error) {
      status.textContent = `Failed: ${error.message}`;
      status.className = 'error';
    } finally {
      button.disabled = false;
      button.textContent = 'Add Court';
    }
  });
}

// Handle login
async function handleLogin(e) {
  e.preventDefault();
  const button = e.target.querySelector('button');
  const status = document.getElementById('login-status');
  
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  
  button.disabled = true;
  button.textContent = 'Logging in...';
  
  try {
    const response = await fetch(`${USER_SERVICE_URL}/users/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }
    
    const data = await response.json();
    authToken = data.access_token;
    localStorage.setItem('tennis_auth_token', authToken);
    
    // Get user info
    await verifyToken();
    
    showStatus('login-status', 'Login successful!', 'success');
    e.target.reset();
    
  } catch (error) {
    showStatus('login-status', `Login failed: ${error.message}`, 'error');
  } finally {
    button.disabled = false;
    button.textContent = 'Login';
  }
}

// Handle registration
async function handleRegister(e) {
  e.preventDefault();
  const button = e.target.querySelector('button');
  const status = document.getElementById('register-status');
  
  const name = document.getElementById('register-name').value;
  const email = document.getElementById('register-email').value;
  const role = document.getElementById('register-role').value;
  const password = document.getElementById('register-password').value;
  
  button.disabled = true;
  button.textContent = 'Registering...';
  
  try {
    const response = await fetch(`${USER_SERVICE_URL}/users/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, email, role, password })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }
      showStatus('register-status', 'Registration successful! Please login.', 'success');
    e.target.reset();
    
    // Switch to login tab
    setTimeout(() => {
      switchTab('login');
    }, 1500);
    } catch (error) {
    showStatus('register-status', `Registration failed: ${error.message}`, 'error');
  } finally {
    button.disabled = false;
    button.textContent = 'Register';
  }
}

// Load initial data
async function loadInitialData() {
  await fetchCourts();
}

// Fetch and display courts
async function fetchCourts() {
  try {
    const response = await fetch(`${COURT_SERVICE_URL}/courts/public`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
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
  courts = data;
  renderCourtSelect();
  renderCourts();
}

function renderCourts() {
  const courtsList = document.getElementById('courts-list');
  if (!courtsList) return;
  
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
  if (!authToken) return;
  
  try {
    const response = await fetch(`${BOOKING_SERVICE_URL}/bookings/`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
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
  bookings = data.filter(booking => booking.user_id === currentUser?.id || booking.booking_by === currentUser?.id);
  renderBookings();
}

function renderBookings() {
  const bookingsList = document.getElementById('bookings-list');
  if (!bookingsList) return;
  
  if (!bookings.length) {
    bookingsList.innerHTML = '<div class="booking-item">No bookings yet. Book a court to get started!</div>';
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
  
  if (!authToken || !currentUser) {
    showStatus('booking-status', 'Please login first to make a booking', 'error');
    return;
  }
  
  const button = e.target.querySelector('button');
  const courtId = e.target.querySelector('#booking-court').value;
  const date = e.target.querySelector('#booking-date').value;
  const time = e.target.querySelector('#booking-time').value;
  const duration = parseInt(e.target.querySelector('#booking-duration').value);

  if (!courtId || !date || !time || !duration) {
    showStatus('booking-status', 'Please fill in all fields', 'error');
    return;
  }

  button.disabled = true;
  button.textContent = 'Booking...';

  try {
    const bookingData = {
      user_id: currentUser.id,
      court_id: courtId,
      time_slot: time,
      duration: duration,
      booking_date: new Date(date).toISOString(),
      booking_by: currentUser.id,
      status: "pending",
      payment_status: "unpaid",
      confirmation_code: generateConfirmationCode()
    };

    const response = await fetch(`${BOOKING_SERVICE_URL}/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify(bookingData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Booking failed');
    }
    
    showStatus('booking-status', 'Booking created successfully!', 'success');
    e.target.reset();
    await fetchBookings(); // Refresh bookings list
    
  } catch (error) {
    showStatus('booking-status', `Failed to create booking: ${error.message}`, 'error');
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

function showStatus(elementId, message, type) {
  const status = document.getElementById(elementId);
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

// Make functions available globally for onclick handlers
window.switchTab = switchTab;
window.logout = logout;
