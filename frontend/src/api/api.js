import axios from 'axios';

// base URL for API requests. In development we proxy `/api` through Vite
// so the frontend can talk to the Django backend without CORS or needing to
// hard‑code a host/port. `VITE_API_URL` can override this (useful for
// production builds).
const API_URL = import.meta.env.VITE_API_URL || '/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/register/', userData),
  login: async (credentials) => {
    const response = await api.post('/token/', credentials);
    if (response.data.access) {
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      // username and flags included by custom serializer
      if (response.data.username) {
        localStorage.setItem('username', response.data.username);
      }
      if (typeof response.data.is_staff !== 'undefined') {
        localStorage.setItem('is_staff', response.data.is_staff);
      }
      if (typeof response.data.is_superuser !== 'undefined') {
        localStorage.setItem('is_superuser', response.data.is_superuser);
      }
    }
    return response;
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    localStorage.removeItem('is_staff');
    localStorage.removeItem('is_superuser');
  },
};

// Doctors API
export const doctorsAPI = {
  getAll: () => api.get('/doctors/'),
  getById: (id) => api.get(`/doctors/${id}/`),
  create: (data) => api.post('/doctors/create/', data),
  update: (id, data) => api.patch(`/doctors/${id}/`, data),
  delete: (id) => api.delete(`/doctors/${id}/`),
};

// Appointments API
export const appointmentsAPI = {
  create: (appointmentData) => api.post('/appointments/', appointmentData),
  getAll: () => api.get('/appointments/'),
  getMyAppointments: () => api.get('/my-appointments/'),
  getById: (id) => api.get(`/appointments/${id}/`),
  update: (id, data) => api.patch(`/appointments/${id}/`, data),
  delete: (id) => api.delete(`/appointments/${id}/`),

  // admin endpoints
  adminList: () => api.get('/admin/appointments/'),
  adminUpdate: (id, data) => api.patch(`/admin/appointments/${id}/`, data),
};

export default api;
