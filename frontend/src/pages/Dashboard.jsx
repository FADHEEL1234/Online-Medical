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
      <h1>Karibu, {username}!</h1>
      <p>Simamia miadi yako ya matibabu kwa urahisi</p>
      
      <div className="quick-actions">
        <div className="action-card" onClick={() => navigate('/doctors')}>
          <h3>Madaktari</h3>
          <p>Angalia orodha ya madaktari waliopo</p>
        </div>
        
        <div className="action-card" onClick={() => navigate('/book-appointment')}>
          <h3>Weka appointment</h3>
          <p>Chagua daktari na muda wa kumuona</p>
        </div>
        
        <div className="action-card" onClick={() => navigate('/my-appointments')}>
          <h3>Appointments zangu</h3>
          <p>Angalia status na historia ya miadi yako</p>
        </div>
        {localStorage.getItem('is_staff') === 'true' && (
          <div className="action-card" onClick={() => navigate('/admin')}>
            <h3>Admin Panel</h3>
            <p>Simamia users, doctors na appointments</p>
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
