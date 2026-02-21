# Online Medical Appointment System

A full-stack web application for booking medical appointments.

## Project Structure

```
medical-system/
├── backend/              # Django REST API
│   ├── backend/          # Django project settings
│   ├── appointments/      # Django app for appointments
│   ├── requirements.txt   # Python dependencies
│   └── manage.py         # Django management script
└── frontend/             # React Application (Vite)
    ├── src/
    │   ├── pages/        # React pages (Register, Login, Dashboard, etc.)
    │   ├── components/   # React components (Navbar)
    │   ├── api/         # API utilities
    │   └── App.jsx      # Main App component
    ├── package.json     # Node dependencies
    └── vite.config.js  # Vite configuration
```

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework, SQLite, JWT Authentication
- **Frontend**: React 18 (Vite), Axios, React Router DOM 6

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Backend Setup

### Step 1: Navigate to backend folder
```
bash
cd medical-system/backend
```

### Step 2: Create virtual environment
```
bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### Step 3: Activate virtual environment
```
bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 4: Install dependencies
```
bash
pip install -r requirements.txt
```

### Step 5: Run migrations
```
bash
python manage.py migrate
```

### Step 6: Create superuser (optional - for admin panel)
```
bash
python manage.py createsuperuser
```

### Step 7: Run the backend server
```
bash
python manage.py runserver
```

Backend will run at: http://localhost:8000

### Step 8: Create sample doctors (Optional)

You can create doctors through the admin panel at http://localhost:8000/admin/ after creating a superuser, or use Django shell:

#### Admin dashboard information

The project now includes a **custom admin dashboard** in the React frontend. Staff users who log in via the normal login form are automatically redirected to `/admin` instead of the regular dashboard. From there an administrator can (the dashboard is mobile‑friendly – all actions are padded/selectable so they work on touch screens):

- Add, update or remove doctors (including setting their daily availability times)
- View every appointment and change its status (approve/reject)

  > Booking clients will see each doctor's available hours when they choose a doctor and the backend rejects any reservations outside that window.

To try this yourself, either create a superuser with `python manage.py createsuperuser` or make an existing user a staff member by running the Django shell and setting `user.is_staff = True` followed by `user.save()`.

(Note: the default Django admin at `/admin/` remains available for superusers.)

```
bash
python manage.py shell
```

Then in the Python shell:
```
python
from appointments.models import Doctor
Doctor.objects.create(name='Dr. John Smith', specialization='Cardiology', email='john@example.com', phone='1234567890')
Doctor.objects.create(name='Dr. Sarah Johnson', specialization='Dermatology', email='sarah@example.com', phone='9876543210')
Doctor.objects.create(name='Dr. Mike Brown', specialization='General Medicine', email='mike@example.com', phone='5551234567')
exit()
```

## Frontend Setup

### Step 1: Navigate to frontend folder
```
bash
cd medical-system/frontend
```

### Step 2: Install dependencies
```
bash
npm install
```

### Step 3: Run the frontend
```
bash
npm run dev
```

Frontend will run at: http://localhost:5173

## Running Both Backend and Frontend

You need to run both servers in separate terminals:

**Terminal 1 (Backend):**
```
bash
cd medical-system/backend
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # Linux/Mac
python manage.py runserver
```

**Terminal 2 (Frontend):**
```
bash
cd medical-system/frontend
npm run dev
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|--------------|
| POST | `/api/register/` | User Registration | No |
| POST | `/api/token/` | Login (Get JWT Token) | No |
| POST | `/api/token/refresh/` | Refresh JWT Token | No |
| GET | `/api/doctors/` | List all doctors | No |
| GET | `/api/doctors/<id>/` | Get doctor details | No |
| **Admin-only** POST | `/api/doctors/create/` | Create a new doctor (set start/end availability) | Yes (staff) |
| **Admin-only** PATCH/DELETE | `/api/doctors/<id>/` | Update or remove a doctor (including availability) | Yes (staff) |
| POST | `/api/appointments/` | Book appointment | Yes |
| GET | `/api/appointments/` | List user's appointments | Yes |
| GET | `/api/my-appointments/` | Get current user's appointments | Yes |
| **Admin-only** GET | `/api/admin/appointments/` | List all appointments | Yes (staff) |
| **Admin-only** PATCH | `/api/admin/appointments/<id>/` | Update any appointment (change status – status field is writable for staff) | Yes (staff) |

## How to Use the Application

1. **Register**: Go to Register page and create an account (make sure the backend server is running on port 8000; the form now checks password match before submitting)
2. **Login**: Login with your credentials
3. **Dashboard**: View the main dashboard with quick actions
4. **View Doctors**: Browse available doctors on the Doctors page
5. **Book Appointment**: Select a doctor and book an appointment
6. **My Appointments**: View your booked appointments and their status (Pending/Approved/Rejected)

## Features

### Backend Features
- ✅ User registration with validation
- ✅ JWT authentication (login/logout)
- ✅ Doctor listing (public access)
- ✅ Appointment booking (authenticated users only)
- ✅ View own appointments
- ✅ SQLite database
- ✅ CORS enabled for React connection

### Frontend Features
- ✅ User registration page
- ✅ User login page with JWT storage
- ✅ Dashboard with quick actions
- ✅ View all doctors
- ✅ Book appointments
- ✅ View and manage appointments
- ✅ Clean and simple UI with CSS
- ✅ Protected routes (redirect to login if not authenticated)

## Troubleshooting

### Frontend not connecting to backend
- Make sure both servers are running
- Check that backend is running on http://localhost:8000
- Check that frontend proxy is configured in vite.config.js

### CORS errors
- Ensure CORS settings in backend/settings.py allow all origins during development (already configured)

### Front‑end/Back‑end connectivity
The React app now proxies `/api` to the Django server (see `frontend/vite.config.js`) and
`frontend/src/api/api.js` defaults to using a relative path or a `VITE_API_URL`
variable. That means you only need to start the backend at \`localhost:8000\` and
run the Vite development server; requests will automatically be routed to the
API and the “Unable to contact server” error can only appear if the backend
process isn’t running or the port is blocked.

There is also a lightweight `/api/health/` endpoint which the front‑end
can ping to verify that the server is up, and the registration page will
show a clear message if the backend cannot be reached.

### Database issues
- Delete db.sqlite3 and run migrations again:
```
bash
rm db.sqlite3
python manage.py migrate
```

### Node modules issues
- Delete node_modules and reinstall:
```
bash
rm -rf node_modules
npm install
```

## Project Files Summary

### Backend Files
- `backend/settings.py` - Django settings with REST Framework and JWT config
- `backend/urls.py` - Main URL routing
- `appointments/models.py` - Doctor and Appointment models
- `appointments/serializers.py` - DRF serializers
- `appointments/views.py` - API views
- `appointments/urls.py` - App URL routing
- `appointments/admin.py` - Admin configuration

### Frontend Files
- `src/App.jsx` - Main app with routing
- `src/api/api.js` - Axios API utility
- `src/pages/Register.jsx` - Registration page
- `src/pages/Login.jsx`/`src/components/Navbar.jsx` - after login the app stores your username and shows a welcome message on dashboard and in the navbar
- `src/pages/Login.jsx` - Login page
- `src/pages/Dashboard.jsx` - Dashboard page
- `src/pages/Doctors.jsx` - Doctors list page
- `src/pages/BookAppointment.jsx` - Book appointment page
- `src/pages/MyAppointments.jsx` - User appointments page
- `src/components/Navbar.jsx` - Navigation component
"# Medical" 
