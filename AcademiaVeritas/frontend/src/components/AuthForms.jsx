import React, { useState } from 'react';
import { registerInstitution, loginInstitution, registerVerifier, loginVerifier } from '../apiService.js';
import { useAuth } from '../context/AuthContext.jsx';

const AuthForms = ({ userType }) => {
  const [activeTab, setActiveTab] = useState('login');
  const [formData, setFormData] = useState({});
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleInputChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);
    
    try {
      if (activeTab === 'register') {
        const apiCall = userType === 'institution' ? registerInstitution : registerVerifier;
        await apiCall(formData);
        setSuccess('Registration successful! Please switch to the login tab.');
        setFormData({});
      } else {
        const apiCall = userType === 'institution' ? loginInstitution : loginVerifier;
        const response = await apiCall(formData);
        login(response.data.token);
      }
    } catch (err) {
      console.error('Authentication error:', err);
      if (err.code === 'ERR_NETWORK' || err.message.includes('Network Error')) {
        setError('Cannot connect to server. Please ensure the backend is running on port 5001.');
      } else if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.response?.status) {
        setError(`Server error (${err.response.status}): ${err.response.statusText}`);
      } else {
        setError(`Connection error: ${err.message || 'An unknown error occurred'}`);
      }
    } finally {
      setIsLoading(false);
    }
  };
  
  const inputStyles = "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors";

  // Google login handler
  const handleGoogleLogin = () => {
    const backendBase = 'http://localhost:5001';
    if (userType === 'institution') {
      window.location.href = `${backendBase}/login/institution/google`;
    } else {
      window.location.href = `${backendBase}/login/verifier/google`;
    }
  };

  return (
    <div className="card max-w-md mx-auto">
      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200 mb-6">
        <button
          onClick={() => setActiveTab('login')}
          className={`px-6 py-3 font-medium text-sm border-b-2 transition-colors ${
            activeTab === 'login'
              ? 'border-primary-500 text-primary-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Login
        </button>
        <button
          onClick={() => setActiveTab('register')}
          className={`px-6 py-3 font-medium text-sm border-b-2 transition-colors ${
            activeTab === 'register'
              ? 'border-primary-500 text-primary-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Register
        </button>
      </div>

      {/* Google Login Button (only on Login tab) */}
      {activeTab === 'login' && (
        <button
          type="button"
          onClick={handleGoogleLogin}
          className="w-full flex items-center justify-center gap-2 mb-6 py-3 border border-gray-300 rounded-lg bg-white hover:bg-gray-50 transition-colors shadow-sm font-medium text-gray-700"
        >
          <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" className="w-5 h-5" />
          Login with Google
        </button>
      )}

      {/* Message Display */}
      {error && (
        <div className="mb-6 p-4 rounded-lg bg-accent-50 text-accent-700 border border-accent-200">
          {error}
        </div>
      )}
      {success && (
        <div className="mb-6 p-4 rounded-lg bg-secondary-50 text-secondary-700 border border-secondary-200">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {activeTab === 'register' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {userType === 'institution' ? 'Institution Name' : 'Name'}
            </label>
            <input
              type="text"
              name="name"
              value={formData.name || ''}
              onChange={handleInputChange}
              className={inputStyles}
              placeholder={userType === 'institution' ? 'Jharkhand University' : 'John Doe'}
              required
            />
          </div>
        )}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <input
            type="email"
            name="email"
            value={formData.email || ''}
            onChange={handleInputChange}
            className={inputStyles}
            placeholder="user@example.com"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input
            type="password"
            name="password"
            value={formData.password || ''}
            onChange={handleInputChange}
            className={inputStyles}
            placeholder="Enter your password"
            required
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full btn-primary py-3 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Processing...' : (activeTab === 'login' ? 'Login' : 'Register')}
        </button>
      </form>
    </div>
  );
};

export default AuthForms;

