import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../api/api';
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
      <div className="login-heading">
        <span className="login-kicker">Medical appointment system</span>
        <h2>Ingia kwenye account</h2>
        <p>Admin ataenda kwenye admin dashboard, user ataenda kwenye dashboard yake.</p>
      </div>
      
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
            {loading ? 'Inaingia...' : 'Login'}
          </button>
      </form>

      <p className="login-footer">
        Huna account? <Link to="/register" className="register-link">Register hapa</Link>
      </p>
    </div>
  );
}

export default Login;
