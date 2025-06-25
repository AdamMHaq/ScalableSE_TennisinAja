# 🎾 TennisinAja - Scalable Tennis Court Booking System

## 👥 Team Members
- Adam Maulana Haq — 23/511623/PA/21832
- Muhammad Naufal Zahir — 23/511471/PA/21804

---

## 📌 Overview

**TennisinAja** is a microservices-based tennis court booking platform designed for real-world use. The system supports user authentication, court management, and booking operations, all accessible via a modern web frontend. Each service is independently deployable and fully containerized with Docker.

---

## 🏗️ Architecture

**Services:**
- **User Service** (`localhost:8000`): User registration, login, JWT authentication, and profile management.
- **Court Service** (`localhost:8001`): CRUD operations for tennis courts, including admin-only endpoints.
- **Booking Service** (`localhost:8002`): Bookings management, including creation, update, and cancellation.
- **Frontend** (`localhost:3000`): Web interface for users and admins.
- **MongoDB** (`localhost:27017`, `localhost:27018`, `localhost:27019`): Separate databases for each service.

**Service Communication:**
- All backend services communicate via REST APIs.
- JWT tokens are used for authentication and authorization across services.

**Deployment:**
- All services and databases are orchestrated using Docker Compose for easy local development and deployment.

---

## 🗂️ Project Structure

```
TennisinAja/
├── docker-compose.yml
├── README.md
├── user_service/         # User management microservice
├── court_service/        # Court management microservice
├── booking_service/      # Booking management microservice
├── frontend/             # Static frontend (HTML/JS/CSS)
    ├── public/
    └── src/
```

---

## 🎯 Key Features

### ** 🔐 Authentication & Authorization System **
- JWT-based Authentication: Secure token-based login with role-based access control
- User Registration & Management: Complete user lifecycle with email validation
- Role-based Security: Admin vs Player permissions with protected endpoints
- Session Persistence: Auto-login with token storage and validation
### ** 🏟️ Court Management System **
- Public Court Discovery: Browse available courts without authentication
- Advanced Filtering: Search by surface type (hard/clay/grass), indoor/outdoor, price range
- Admin Court Creation: Full CRUD operations for court administrators
- Rich Court Data: Comprehensive court info including pricing, contact, Google Maps integration
- Real-time Updates: Instant court availability across all users
### ** 📅 Booking Management System **
- Smart Booking Engine: Prevents double-booking with time slot validation
- Multi-duration Support: 1-3 hour booking slots with flexible scheduling
- Booking History: Complete booking lifecycle tracking (pending → confirmed → cancelled)
- Payment Status Tracking: Integrated payment status management (unpaid → paid → refunded)
- Confirmation Codes: Unique booking identifiers for verification
### 🛡️ ** Security & Reliability **
- Password Encryption: Bcrypt hashing for secure password storage
- CORS Configuration: Proper cross-origin resource sharing setup
- Input Validation: Comprehensive request validation with Pydantic models
- Error Handling: Graceful error responses with proper HTTP status codes
- Token Expiration: Automatic JWT token lifecycle management

---

## 🚀 Quick Start

### 1. Start All Services

```bash
docker-compose up --build
```

- User Service → [http://localhost:8000](http://localhost:8000)
- Court Service → [http://localhost:8001](http://localhost:8001)
- Booking Service → [http://localhost:8002](http://localhost:8002)
- Frontend → [http://localhost:3000](http://localhost:3000)

### 2. Demo Accounts

- **Admin:**  
  Email: `admin@tennisinaja.com`  
  Password: `admin123`
- **Player:**  
  Email: `john.doe@example.com`  
  Password: `player123`

### 3. Using the App

- Open [http://localhost:3000](http://localhost:3000)
- Login as admin to add courts, or as player to book courts.
- Courts and bookings are visible and manageable via the web UI.

---

## 🔑 API Endpoints

### User Service (`localhost:8000`)
- `POST /users/register` — Register new user
- `POST /users/login` — Login and get JWT token
- `GET /users/me` — Get current user profile (requires JWT)
- `GET /users/` — List all users (admin only)
- `GET /users/{user_id}` — Get user by ID

### Court Service (`localhost:8001`)
- `GET /courts/public` — List all public courts (no auth)
- `GET /courts/` — List all courts (admin only)
- `POST /courts/` — Add new court (admin only)
- `GET /courts/{court_id}` — Get court details
- `PUT /courts/{court_id}` — Update court (admin only)
- `DELETE /courts/{court_id}` — Delete court (admin only)

### Booking Service (`localhost:8002`)
- `GET /bookings/` — List all bookings (auth required)
- `POST /bookings/` — Create new booking (auth required)
- `GET /bookings/{booking_id}` — Get booking details (auth required)
- `PUT /bookings/{booking_id}` — Update booking (auth required)
- `DELETE /bookings/{booking_id}` — Cancel booking (auth required)

---

## 🛠️ Technology Stack

| Layer      | Technology                                      |
|------------|-------------------------------------------------|
| Frontend   | HTML, CSS, JavaScript (Vanilla), Serve (Node)   |
| Backend    | Python 3.12, FastAPI, Uvicorn                   |
| Database   | MongoDB (separate DBs per service)              |
| Auth       | JWT (python-jose), bcrypt password hashing      |
| Deployment | Docker, Docker Compose                          |

---

## 🧩 Development & Customization

### Running a Single Service

```bash
cd user_service
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Environment Variables

- `MONGODB_URL`: MongoDB connection string (see `docker-compose.yml`)
- `SECRET_KEY`: JWT secret key (must match across services)
- `USER_SERVICE_URL`: URL for user service (for inter-service auth)

### Adding New Courts as Admin

- Login as admin on the frontend.
- Use the "Add Court" form to create a new court.
- The court will appear instantly for all users.

---

## 🐳 Docker Compose Services

- **mongo-user**: MongoDB for user service (`localhost:27017`)
- **mongo-court**: MongoDB for court service (`localhost:27018`)
- **mongo-booking**: MongoDB for booking service (`localhost:27019`)
- **user_service**: FastAPI user microservice
- **court_service**: FastAPI court microservice
- **booking_service**: FastAPI booking microservice
- **frontend**: Static web frontend (served on port 3000)

---

## 🎨 Frontend Features

- **Authentication:** Login/register with JWT, role-based UI.
- **Court Management:** Admins can add, edit, and delete courts.
- **Booking:** Players can view available courts and make/cancel bookings.
- **Responsive Design:** Works on desktop and mobile.

---

## 🧪 Testing & Troubleshooting

- **Check Service Health:**  
  ```
  curl http://localhost:8000/
  curl http://localhost:8001/
  curl http://localhost:8002/
  ```
- **Check MongoDB Data:**  
  Use MongoDB Compass or shell to inspect collections.
- **Frontend Not Showing Data?**  
  - Ensure backend services are running.
  - Check browser console for API errors.
  - Verify MongoDB contains the expected data.

---

## 💡 Development Notes

- **Microservices:** Each service is fully decoupled and can be scaled independently.
- **Security:** JWT tokens are validated on every protected endpoint.
- **CORS:** Enabled for all services to allow frontend-backend communication.
- **Mock Data:** Each service loads demo data on startup for easy testing.

---

## 🚦 Future Enhancements

- Email notifications for bookings
- Payment integration
- Calendar view for bookings
- Admin analytics dashboard
- Mobile app

---

**Enjoy booking your next tennis match with TennisinAja!**
