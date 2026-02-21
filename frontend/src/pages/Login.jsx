import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api, { authAPI } from '../api/api';
import useBackendStatus from '../hooks/useBackendStatus';

function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
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
      setError('Cannot log in because backend is not reachable');
      return;
    }
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const resp = await authAPI.login(formData);
      const isStaff = resp.data.is_staff;
      if (isStaff) {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="card login-card">
      <h2>Login</h2>
      
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
          <label htmlFor="password">Password *</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !backendUp}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
      </form>

      <p className="login-footer">
        Don't have an account? <Link to="/register" className="register-link">Register here</Link>
      </p>
    </div>
  );
}

export default Login;
