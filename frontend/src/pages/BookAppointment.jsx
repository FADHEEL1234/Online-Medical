import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { doctorsAPI, appointmentsAPI } from '../api/api';
import useBackendStatus from '../hooks/useBackendStatus';

function BookAppointment() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { backendUp, error: backendError } = useBackendStatus();

  const [formData, setFormData] = useState({
    doctor: searchParams.get('doctor') || '',
    appointment_date: '',
  });

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

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const selectedDoctor = doctors.find(d => d.id === parseInt(formData.doctor));
    if (selectedDoctor && formData.appointment_date) {
      const apptDate = new Date(formData.appointment_date);
      const hhmm = apptDate.toTimeString().slice(0,5);
      if (hhmm < selectedDoctor.available_from || hhmm > selectedDoctor.available_to) {
        setError("Selected time is outside doctor's availability");
        return;
      }
    }

    setSubmitting(true);
    try {
      await appointmentsAPI.create(formData);
      setSuccess('Appointment booked successfully!');
      setTimeout(() => {
        navigate('/my-appointments');
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to book appointment. Please try again.');
    } finally {
      setSubmitting(false);
    }
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
        <h2>Book an Appointment</h2>
        
        {backendError && <div className="message message-error">{backendError}</div>}
        {error && <div className="message message-error">{error}</div>}
        {success && <div className="message message-success">{success}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="doctor">Select Doctor *</label>
            <select
              id="doctor"
              name="doctor"
              value={formData.doctor}
              onChange={handleChange}
              required
            >
              <option value="">-- Select a Doctor --</option>
              {doctors.map((doctor) => (
                <option key={doctor.id} value={doctor.id}>
                  Dr. {doctor.name} - {doctor.specialization}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="appointment_date">Appointment Date & Time *</label>
            <input
              type="datetime-local"
              id="appointment_date"
              name="appointment_date"
              value={formData.appointment_date}
              onChange={handleChange}
              required
              min={new Date().toISOString().slice(0, 16)}
            />
          </div>
          {formData.doctor && (() => {
            const doc = doctors.find(d => d.id === parseInt(formData.doctor));
            if (doc) {
              return (
                <p style={{ fontSize: '0.9rem' }}>
                  Available: {doc.available_from || 'N/A'} – {doc.available_to || 'N/A'}
                </p>
              );
            }
            return null;
          })()}

          <button 
            type="submit" 
            className="btn btn-primary" 
            disabled={submitting || !backendUp}
          >
            {submitting ? 'Booking...' : 'Book Appointment'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default BookAppointment;
