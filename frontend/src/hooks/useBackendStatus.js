import { useState, useEffect } from 'react';
import api from '../api/api';

// simple hook that probes the health endpoint once and reports whether
// the backend was reachable.  Components can use the returned values to
// disable forms and show a persistent error message.
export default function useBackendStatus() {
  const [backendUp, setBackendUp] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const probe = async () => {
      try {
        await api.get('/health/');
        setBackendUp(true);
      } catch (e) {
        setBackendUp(false);
        setError('Unable to reach backend. Please make sure the Django server is running.');
      }
    };
    probe();
  }, []);

  return { backendUp, error };
}
