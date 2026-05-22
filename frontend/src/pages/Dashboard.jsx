import { authAPI } from '../api/api';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username') || 'User';
  const isStaff = localStorage.getItem('is_staff') === 'true';

  const actions = [
    {
      title: 'Madaktari',
      description: 'Angalia orodha ya madaktari waliopo',
      accent: 'action-card-blue',
      label: 'Angalia sasa',
      onClick: () => navigate('/doctors'),
    },
    {
      title: 'Weka appointment',
      description: 'Chagua daktari na muda wa kumuona',
      accent: 'action-card-blue',
      label: 'Panga muda',
      onClick: () => navigate('/book-appointment'),
    },
    {
      title: 'Appointments zangu',
      description: 'Angalia status na historia ya miadi yako',
      accent: 'action-card-blue',
      label: 'Fuatilia',
      onClick: () => navigate('/my-appointments'),
    },
  ];

  if (isStaff) {
    actions.push({
      title: 'Admin Panel',
      description: 'Simamia users, doctors na appointments',
      accent: 'action-card-blue',
      label: 'Fungua admin',
      onClick: () => navigate('/admin'),
    });
  }


  const handleLogout = () => {
    authAPI.logout();
    navigate('/login');
  };

  return (
    <div className="welcome-section dashboard-shell">
      <div className="dashboard-hero">
        <div className="dashboard-hero-copy">
          <span className="dashboard-kicker">Dashboard ya mtumiaji</span>
          <h1>Karibu, {username}!</h1>
          <p>Simamia miadi yako ya matibabu kwa urahisi, kwa muonekano wenye motion safi na navigation ya haraka.</p>

          <div className="dashboard-pills">
            <span className="dashboard-pill">Miadi kwa hatua chache</span>
            <span className="dashboard-pill">Ufuatiliaji wa status</span>
            <span className="dashboard-pill">Madaktari waliopo</span>
          </div>
        </div>

        <div className="dashboard-spotlight" aria-hidden="true">
          <div className="spotlight-orb spotlight-orb-primary"></div>
          <div className="spotlight-orb spotlight-orb-secondary"></div>
          <div className="spotlight-card">
            <span>Huduma za haraka</span>
            <strong>{actions.length} sehemu muhimu</strong>
            <small>Chagua unachotaka kufanya sasa</small>
          </div>
        </div>
      </div>

      <div className="quick-actions dashboard-grid">
        {actions.map((action) => (
          <button
            key={action.title}
            type="button"
            className={`action-card ${action.accent}`}
            onClick={action.onClick}
          >
            <span className="action-card-label">{action.label}</span>
            <h3>{action.title}</h3>
            <p>{action.description}</p>
          </button>
        ))}
      </div>

      <div className="dashboard-footer-actions">
        <button onClick={handleLogout} className="btn btn-secondary dashboard-logout">
          Logout
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
