import { Link, useNavigate, useLocation } from 'react-router-dom';
import { authAPI } from '../api/api';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthenticated = localStorage.getItem('token') !== null;

  const handleLogout = () => {
    authAPI.logout();
    navigate('/login');
  };

  if (!isAuthenticated) {
    return null;
  }

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  const username = localStorage.getItem('username') || '';

  return (
    <nav style={navStyle}>
      <div style={navContainerStyle}>
        <Link to="/dashboard" style={logoStyle}>
          Medical Appointments
        </Link>
        {username && <span style={greetingStyle}>Welcome, {username}</span>}
        <ul style={navLinksStyle}>
          <li>
            <Link to="/dashboard" style={isActive('/dashboard') ? activeLinkStyle : linkStyle}>
              Dashboard
            </Link>
          </li>
          <li>
            <Link to="/doctors" style={isActive('/doctors') ? activeLinkStyle : linkStyle}>
              Doctors
            </Link>
          </li>
          <li>
            <Link to="/book-appointment" style={isActive('/book-appointment') ? activeLinkStyle : linkStyle}>
              Book Appointment
            </Link>
          </li>
          <li>
            <Link to="/my-appointments" style={isActive('/my-appointments') ? activeLinkStyle : linkStyle}>
              My Appointments
            </Link>
          </li>
          {localStorage.getItem('is_staff') === 'true' && (
            <li>
              <Link to="/admin" style={isActive('/admin') ? activeLinkStyle : linkStyle}>
                Admin
              </Link>
            </li>
          )}
          <li>
            <button onClick={handleLogout} style={logoutButtonStyle}>
              Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

const navStyle = {
  backgroundColor: '#007bff',
  padding: '15px 0',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
};

const navContainerStyle = {
  maxWidth: '1200px',
  margin: '0 auto',
  padding: '0 20px',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
};

const logoStyle = {
  color: 'white',
  fontSize: '20px',
  fontWeight: 'bold',
  textDecoration: 'none',
};

const navLinksStyle = {
  display: 'flex',
  listStyle: 'none',
  gap: '20px',
  alignItems: 'center',
  margin: 0,
  padding: 0,
};

const linkStyle = {
  color: 'white',
  textDecoration: 'none',
  padding: '8px 12px',
  borderRadius: '4px',
  transition: 'background-color 0.2s',
};

const activeLinkStyle = {
  color: 'white',
  textDecoration: 'none',
  padding: '8px 12px',
  borderRadius: '4px',
  backgroundColor: '#0056b3',
};

const logoutButtonStyle = {
  backgroundColor: '#dc3545',
  color: 'white',
  border: 'none',
  padding: '8px 16px',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '14px',
};

const greetingStyle = {
  color: 'white',
  marginLeft: '20px',
  fontSize: '16px',
};

export default Navbar;
