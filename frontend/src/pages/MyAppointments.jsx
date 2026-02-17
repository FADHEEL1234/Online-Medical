import { useState, useEffect } from 'react';
import { appointmentsAPI } from '../api/api';
import useBackendStatus from '../hooks/useBackendStatus';

function MyAppointments() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { backendUp, error: backendError } = useBackendStatus();

  useEffect(() => {
    if (backendUp) {
      fetchAppointments();
    } else {
      setError(backendError);
      setLoading(false);
    }
  }, [backendUp, backendError]);

  const fetchAppointments = async () => {
    try {
      const response = await appointmentsAPI.getMyAppointments();
      setAppointments(response.data);
    } catch (err) {
      setError('Failed to load appointments. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (id) => {
    if (window.confirm('Are you sure you want to cancel this appointment?')) {
      try {
        await appointmentsAPI.delete(id);
        fetchAppointments();
      } catch (err) {
        alert('Failed to cancel appointment. Please try again.');
      }
    }
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'Approved':
        return 'status-badge status-approved';
      case 'Rejected':
        return 'status-badge status-rejected';
      default:
        return 'status-badge status-pending';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
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
        <h2>My Appointments</h2>
        
        {backendError && <div className="message message-error">{backendError}</div>}
        {error && <div className="message message-error">{error}</div>}
        
        {appointments.length === 0 ? (
          <p>You haven't booked any appointments yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Doctor</th>
                <th>Specialization</th>
                <th>Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((appointment) => (
                <tr key={appointment.id}>
                  <td>Dr. {appointment.doctor_name}</td>
                  <td>{appointment.doctor_specialization}</td>
                  <td>{formatDate(appointment.appointment_date)}</td>
                  <td>
                    <span className={getStatusBadgeClass(appointment.status)}>
                      {appointment.status}
                    </span>
                  </td>
                  <td>
                    {appointment.status === 'Pending' && (
                      <button 
                        className="btn btn-danger"
                        onClick={() => handleCancel(appointment.id)}
                      >
                        Cancel
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default MyAppointments;
