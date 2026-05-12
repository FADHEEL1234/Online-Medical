import { useState, useEffect } from 'react';
import api, { doctorsAPI, appointmentsAPI, usersAPI } from '../api/api';
import { useNavigate } from 'react-router-dom';

function AdminDashboard() {
  const navigate = useNavigate();
  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [users, setUsers] = useState([]);
  const [newDoctor, setNewDoctor] = useState({ name: '', specialization: '', email: '', phone: '', available_from: '09:00', available_to: '17:00', available_days: [] });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [docResp, apptResp, userResp] = await Promise.all([
        doctorsAPI.getAll(),
        appointmentsAPI.adminList(),
        usersAPI.adminList()
      ]);
      setDoctors(docResp.data);
      setAppointments(apptResp.data);
      setUsers(userResp.data);
    } catch (err) {
      setError('Failed to load admin data');
    }
  };

  const handleDoctorChange = (e) => {
    setNewDoctor({ ...newDoctor, [e.target.name]: e.target.value });
  };

  const toggleAvailableDay = (day) => {
    const days = new Set(newDoctor.available_days || []);
    if (days.has(day)) days.delete(day); else days.add(day);
    setNewDoctor({ ...newDoctor, available_days: Array.from(days).sort((a,b)=>a-b) });
  };

  const handleDoctorSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      if (editingId) {
        await doctorsAPI.update(editingId, newDoctor);
        setEditingId(null);
      } else {
        await doctorsAPI.create(newDoctor);
      }
      setNewDoctor({ name: '', specialization: '', email: '', phone: '', available_from: '09:00', available_to: '17:00', available_days: [] });
      fetchData();
    } catch (err) {
      setError(err.response?.data || 'Error saving doctor');
    } finally {
      setLoading(false);
    }
  };

  const changeAppointmentStatus = async (id, status) => {
    try {
      await api.patch(`/admin/appointments/${id}/`, { status });
      fetchData();
    } catch (err) {
      setError('Could not update appointment');
    }
  };

  const formatDate = (dateValue) => {
    if (!dateValue) return 'Not logged in yet';
    return new Date(dateValue).toLocaleString();
  };

  const getRole = (user) => {
    if (user.is_superuser) return 'Super admin';
    if (user.is_staff) return 'Admin';
    return 'User';
  };

  return (
    <div className="admin-dashboard">
      <h1>Admin dashboard</h1>
      {error && <div className="message message-error">{error}</div>}

      <section className="admin-section">
        <h2>Registered users</h2>
        <div className="admin-summary">
          <span>Total users: {users.length}</span>
          <span>Logged in users: {users.filter((user) => user.last_login).length}</span>
        </div>
        <table className="admin-table users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Registered</th>
              <th>Last login</th>
              <th>Appointments</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.full_name}</td>
                <td>{user.username}</td>
                <td>{user.email || '-'}</td>
                <td>{getRole(user)}</td>
                <td>{formatDate(user.date_joined)}</td>
                <td>{formatDate(user.last_login)}</td>
                <td>{user.appointment_count}</td>
              </tr>
            ))}
            {users.length === 0 && (
              <tr>
                <td colSpan="8">No registered users found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>

      <section className="admin-section">
        <h2>Doctors</h2>
        <form onSubmit={handleDoctorSubmit} className="admin-form">
          <label>
            Name
            <input name="name" placeholder="Name" value={newDoctor.name} onChange={handleDoctorChange} required />
          </label>
          <label>
            Specialization
            <input name="specialization" placeholder="Specialization" value={newDoctor.specialization} onChange={handleDoctorChange} required />
          </label>
          <label>
            Email
            <input name="email" placeholder="Email" value={newDoctor.email} onChange={handleDoctorChange} required />
          </label>
          <label>
            Phone
            <input name="phone" placeholder="Phone" value={newDoctor.phone} onChange={handleDoctorChange} required />
          </label>
          <div style={{ display: 'flex', gap: '10px' }}>
            <label>
              From:
              <input type="time" name="available_from" value={newDoctor.available_from} onChange={handleDoctorChange} required />
            </label>
            <label>
              To:
              <input type="time" name="available_to" value={newDoctor.available_to} onChange={handleDoctorChange} required />
            </label>
          </div>
          <div style={{ marginTop: '8px' }}>
            <label style={{ display: 'block', marginBottom: '6px' }}>Available days</label>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].map((label, idx) => (
                <label key={idx} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <input type="checkbox" checked={(newDoctor.available_days||[]).includes(idx)} onChange={() => toggleAvailableDay(idx)} />
                  <span style={{ fontSize: '13px' }}>{label}</span>
                </label>
              ))}
            </div>
          </div>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            <button type="submit" disabled={loading}>
              {loading ? (editingId ? 'Saving...' : 'Adding...') : (editingId ? 'Save changes' : 'Add doctor')}
            </button>
            {editingId && (
              <button type="button" onClick={() => { setEditingId(null); setNewDoctor({ name: '', specialization: '', email: '', phone: '', available_from: '09:00', available_to: '17:00', available_days: [] }); }} className="btn btn-secondary">
                Cancel
              </button>
            )}
          </div>
        </form>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {doctors.map(d => (
            <li key={d.id} style={{ marginBottom: '8px', display: 'flex', alignItems: 'center' }}>
              <span style={{ flex: 1 }}>
                {d.name} ({d.specialization}) – {d.available_from || '??'} to {d.available_to || '??'}
              </span>
              <button
                className="btn"
                style={{ fontSize: '12px' }}
                onClick={() => {
                  setEditingId(d.id);
                  setNewDoctor({
                    name: d.name,
                    specialization: d.specialization,
                    email: d.email,
                    phone: d.phone,
                    available_from: d.available_from ? d.available_from.slice(0,5) : '09:00',
                    available_to: d.available_to ? d.available_to.slice(0,5) : '17:00',
                    available_days: d.available_days || [],
                  });
                }}
              >
                Edit
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section className="admin-section">
        <h2>Appointments</h2>
        {/*
          The status and action buttons below are designed to be touchable on
          mobile devices.  In addition to the Approve/Reject buttons, you can
          directly change the current status with the dropdown — the entire
          control has been padded and styled for easy tapping.
        */}
        <table className="admin-table">
          <thead>
            <tr>
              <th>ID</th><th>User</th><th>Doctor</th><th>Date</th><th>Status</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {appointments.map(a => (
              <tr key={a.id}>
                <td>{a.id}</td>
                <td>{a.user_name}</td>
                <td>{a.doctor_name}</td>
                <td>{new Date(a.appointment_date).toLocaleString()}</td>
                <td>
            {/* status editable via select for touch devices */}
            <select
              value={a.status}
              onChange={(e) => changeAppointmentStatus(a.id, e.target.value)}
            >
              <option value="Pending">Pending</option>
              <option value="Approved">Approved</option>
              <option value="Rejected">Rejected</option>
            </select>
          </td>
          <td>
            {a.status !== 'Approved' && (
              <button
                className="btn"
                onClick={() => changeAppointmentStatus(a.id, 'Approved')}
                style={{backgroundColor:'#28a745',color:'#fff'}}
              >
                Approve
              </button>
            )}
            {a.status !== 'Rejected' && (
              <button
                className="btn"
                onClick={() => changeAppointmentStatus(a.id, 'Rejected')}
                style={{backgroundColor:'#dc3545',color:'#fff'}}
              >
                Reject
              </button>
            )}
          </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <button className="btn btn-secondary" onClick={() => navigate('/dashboard')}>Back to user dashboard</button>
    </div>
  );
}

export default AdminDashboard;
