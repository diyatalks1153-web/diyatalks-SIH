import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const GoogleAuthHandler = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    if (token) {
      localStorage.setItem('authToken', token);
      // Redirect to dashboard or home page
      navigate('/');
    } else {
      // If no token, redirect to login
      navigate('/');
    }
  }, [navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="text-lg font-semibold">Logging you in with Google...</div>
    </div>
  );
};

export default GoogleAuthHandler;
