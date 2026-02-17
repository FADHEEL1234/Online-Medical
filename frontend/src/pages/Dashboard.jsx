import { Link } from 'react-router-dom';
import { authAPI } from '../api/api';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username') || 'User';

  const handleLogout = () => {
    authAPI.logout();
    navigate('/login');
  };

  return (
    <div className="welcome-section">
      <h1>Welcome, {username}!</h1>
      <p>Manage your medical appointments with ease</p>
      
      <div className="quick-actions">
        <div className="action-card" onClick={() => navigate('/doctors')}>
          <h3>View Doctors</h3>
          <p>Browse our list of specialist doctors</p>
        </div>
        
        <div className="action-card" onClick={() => navigate('/book-appointment')}>
          <h3>Book Appointment</h3>
          <p>Schedule a new appointment with a doctor</p>
        </div>
        
        <div className="action-card" onClick={() => navigate('/my-appointments')}>
          <h3>My Appointments</h3>
          <p>View and manage your appointments</p>
        </div>
        {localStorage.getItem('is_staff') === 'true' && (
          <div className="action-card" onClick={() => navigate('/admin')}>
            <h3>Admin Panel</h3>
            <p>Manage doctors &amp; appointments</p>
          </div>
        )}
      </div>

      <div style={{ marginTop: '40px' }}>
        <button onClick={handleLogout} className="btn btn-secondary">
          Logout
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
