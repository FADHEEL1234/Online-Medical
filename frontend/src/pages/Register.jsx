import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api, { authAPI } from '../api/api';
import useBackendStatus from '../hooks/useBackendStatus';

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { backendUp, error: backendError } = useBackendStatus();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    if (!backendUp) {
      setError('Cannot register because backend is not reachable');
      return;
    }
    e.preventDefault();
    setError('');

    // quick client-side validation to avoid unnecessary requests
    if (formData.password !== formData.password_confirm) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      await authAPI.register(formData);
      alert('Registration successful! Please login.');
      navigate('/login');
    } catch (err) {
      // default generic message
      let message = 'Registration failed. Please try again.';

      // network-level error (backend unreachable)
      if (!err.response) {
        message =
          'Unable to contact server. Please make sure the backend is running';
      } else if (err.response.data) {
        if (err.response.data.detail) {
          message = err.response.data.detail;
        } else {
          // DRF often returns an object with field-specific lists
          const data = err.response.data;
          const parts = [];
          Object.values(data).forEach((v) => {
            if (Array.isArray(v)) {
              parts.push(v.join(' '));
            } else if (typeof v === 'string') {
              parts.push(v);
            }
          });
          if (parts.length) {
            message = parts.join(' ');
          }
        }
      }

      setError(message);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="card" style={{ maxWidth: '500px', margin: '40px auto' }}>
      <h2>Register</h2>
      
      {backendError && <div className="message message-error">{backendError}</div>}
      {error && <div className="message message-error">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        {!backendUp && (
          <div className="message message-error" style={{ marginBottom: '1rem' }}>
            Backend not available – start the server and refresh.
          </div>
        )}
        <div className="form-group">
          <label htmlFor="username">Username *</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email *</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="first_name">First Name</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="last_name">Last Name</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password *</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength="8"
          />
        </div>

        <div className="form-group">
          <label htmlFor="password_confirm">Confirm Password *</label>
          <input
            type="password"
            id="password_confirm"
            name="password_confirm"
            value={formData.password_confirm}
            onChange={handleChange}
            required
            minLength="8"
          />
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          style={{ width: '100%' }}
          disabled={loading || !backendUp}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>

      <p style={{ marginTop: '20px', textAlign: 'center' }}>
        Already have an account? <Link to="/login">Login here</Link>
      </p>
    </div>
  );
}

export default Register;
