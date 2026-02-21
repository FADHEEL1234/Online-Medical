import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { doctorsAPI } from '../api/api';
import useBackendStatus from '../hooks/useBackendStatus';

function Doctors() {
  const navigate = useNavigate();
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { backendUp, error: backendError } = useBackendStatus();

  useEffect(() => {
    if (backendUp) {
      fetchDoctors();
    } else {
      setError(backendError);
      setLoading(false);
    }
  }, [backendUp, backendError]);

  const fetchDoctors = async () => {
    try {
      const response = await doctorsAPI.getAll();
      setDoctors(response.data);
    } catch (err) {
      setError('Failed to load doctors. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleBookAppointment = (doctorId) => {
    navigate(`/book-appointment?doctor=${doctorId}`);
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h2>Our Doctors</h2>
        
        {backendError && <div className="message message-error">{backendError}</div>}
        {error && <div className="message message-error">{error}</div>}
        
        {doctors.length === 0 ? (
          <p>No doctors available at the moment.</p>
        ) : (
          doctors.map((doctor) => (
            <div key={doctor.id} className="doctor-card">
              <h3>Dr. {doctor.name}</h3>
              <p className="specialization">{doctor.specialization}</p>
              <p className="contact">Email: {doctor.email}</p>
              <p className="contact">Phone: {doctor.phone}</p>
              <p className="contact">Available: {doctor.available_from || 'N/A'} – {doctor.available_to || 'N/A'}</p>
              <p className="available-days">Days: {
                (() => {
                  const names = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
                  const days = doctor.available_days || [];
                  if (!days || days.length === 0) return 'N/A';
                  try {
                    const labels = days.map(d => names[parseInt(d, 10)]).filter(Boolean);
                    return labels.map((label, idx) => (
                      <span key={idx} className="day-pill">{label}</span>
                    ));
                  } catch (e) {
                    return 'N/A';
                  }
                })()
              }</p>
              <button 
                className="btn btn-primary" 
                style={{ marginTop: '15px' }}
                onClick={() => handleBookAppointment(doctor.id)}
              >
                Book Appointment
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Doctors;
