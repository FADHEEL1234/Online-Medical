import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../api/api';
import useBackendStatus from '../hooks/useBackendStatus';

function Login2() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [successState, setSuccessState] = useState(null);
  const { backendUp, error: backendError } = useBackendStatus();

  useEffect(() => {
    if (!successState) return;

    const timer = window.setTimeout(() => {
      navigate(successState.redirectTo);
    }, 1800);

    return () => window.clearTimeout(timer);
  }, [navigate, successState]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!backendUp) {
      setError('Cannot log in because backend is not reachable');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const resp = await authAPI.login(formData);
      const isStaff = resp.data.is_staff;

      setSuccessState({
        redirectTo: isStaff ? '/admin' : '/dashboard',
        title: 'Yes! Login successful',
        subtitle: isStaff
          ? 'Unaelekezwa kwenye admin dashboard sasa hivi.'
          : 'Unaelekezwa kwenye dashboard yako sasa hivi.',
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
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
              placeholder="Enter username"
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
              placeholder="Enter password"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !backendUp || Boolean(successState)}
          >
            {loading ? 'Inaingia...' : 'Login'}
          </button>
        </form>

        <p className="login-footer">
          Huna account?{' '}
          <Link to="/register" className="register-link">
            Register hapa
          </Link>
        </p>
      </div>

      {successState && (
        <div className="login-success-overlay" role="status" aria-live="polite">
          <div className="login-success-card">
            <div className="login-success-burst" aria-hidden="true">
              <span className="burst-ring burst-ring-one"></span>
              <span className="burst-ring burst-ring-two"></span>
              <span className="burst-dot burst-dot-one"></span>
              <span className="burst-dot burst-dot-two"></span>
              <span className="burst-dot burst-dot-three"></span>
            </div>
            <div className="login-success-badge" aria-hidden="true">
              <span className="login-success-check"></span>
            </div>
            <h3>{successState.title}</h3>
            <p>{successState.subtitle}</p>
            <span className="login-success-caption">Karibu ndani</span>
          </div>
        </div>
      )}
    </>
  );
}

export default Login2;

