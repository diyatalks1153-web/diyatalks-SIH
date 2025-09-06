import React, { useState, useEffect } from 'react';
import api from '../apiService';

// --- Main Component ---
const InstitutionPortal = () => {
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [isLoggedIn, setIsLoggedIn] = useState(!!token);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setIsLoggedIn(false);
  };

  const handleLoginSuccess = (newToken) => {
    localStorage.setItem('authToken', newToken);
    setToken(newToken);
    setIsLoggedIn(true);
  };

  if (isLoggedIn) {
    return <AddCertificateForm onLogout={handleLogout} />;
  } else {
    return <AuthForms onLoginSuccess={handleLoginSuccess} />;
  }
};


// --- Authentication Forms Component ---

const AuthForms = ({ onLoginSuccess }) => {
  const [activeTab, setActiveTab] = useState('login'); // 'login' or 'register'
  const [userType, setUserType] = useState('institution'); // 'institution' or 'verifier'
  const [formData, setFormData] = useState({});
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLoading) return;
    setError('');
    setSuccess('');
    setIsLoading(true);
    try {
      if (activeTab === 'register') {
        if (userType === 'institution') {
          await api.registerInstitution(formData);
        } else {
          await api.registerVerifier(formData);
        }
        setSuccess('Registration successful! Please log in.');
        setActiveTab('login');
        setFormData({});
      } else {
        let response;
        if (userType === 'institution') {
          response = await api.loginInstitution(formData);
        } else {
          response = await api.loginVerifier(formData);
        }
        onLoginSuccess(response.data.token);
      }
    } catch (err) {
      setError(err.response?.data?.error || err.response?.data?.message || 'An error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  const inputStyles = "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500";

  // Google login handler
  const handleGoogleLogin = () => {
    const endpoint = userType === 'institution'
      ? 'http://localhost:5000/api/institution/google'
      : 'http://localhost:5000/api/verifier/google';
    window.location.href = endpoint;
  };

  return (
    <div className="bg-white p-4 sm:p-8 rounded-lg shadow-lg max-w-md mx-auto">
      <div className="flex border-b mb-4">
        <button onClick={() => setActiveTab('login')} className={`py-2 px-6 font-semibold ${activeTab === 'login' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}>Login</button>
        <button onClick={() => setActiveTab('register')} className={`py-2 px-6 font-semibold ${activeTab === 'register' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}>Register</button>
      </div>
      <div className="flex justify-center mb-6 gap-2">
        <button
          type="button"
          onClick={() => setUserType('institution')}
          className={`px-4 py-1 rounded-full text-sm font-semibold border ${userType === 'institution' ? 'bg-blue-600 text-white border-blue-600' : 'bg-gray-100 text-gray-700 border-gray-300'}`}
        >
          Institution
        </button>
        <button
          type="button"
          onClick={() => setUserType('verifier')}
          className={`px-4 py-1 rounded-full text-sm font-semibold border ${userType === 'verifier' ? 'bg-blue-600 text-white border-blue-600' : 'bg-gray-100 text-gray-700 border-gray-300'}`}
        >
          Verifier
        </button>
      </div>
      <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
        {activeTab === 'login'
          ? (userType === 'institution' ? 'Institution Login' : 'Verifier Login')
          : (userType === 'institution' ? 'Register Institution' : 'Register Verifier')}
      </h2>
      {activeTab === 'login' && (
        <button
          type="button"
          onClick={handleGoogleLogin}
          className="w-full flex items-center justify-center gap-2 py-2 mb-4 border border-gray-300 rounded-lg bg-white hover:bg-gray-100 font-semibold text-gray-700 shadow-sm transition-colors"
        >
          <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" className="w-5 h-5" />
          Login with Google {userType === 'institution' ? 'as Institution' : 'as Verifier'}
        </button>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        {activeTab === 'register' && (
          <div>
            <label className="block text-sm font-medium text-gray-700">
              {userType === 'institution' ? 'Institution Name' : 'Verifier Name'}
            </label>
            <input type="text" name="name" onChange={handleInputChange} className={inputStyles} required />
          </div>
        )}
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" name="email" onChange={handleInputChange} className={inputStyles} required />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" name="password" onChange={handleInputChange} className={inputStyles} required />
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        {success && <p className="text-green-500 text-sm">{success}</p>}
        <button
          type="submit"
          disabled={isLoading}
          className={`w-full font-bold py-2 px-4 rounded-lg transition-colors ${
            isLoading
              ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {isLoading ? 'Processing...' : (activeTab === 'login' ? 'Login' : 'Register')}
        </button>
      </form>
    </div>
  );
};

// --- Add Certificate Form Component (for logged-in users) ---
const AddCertificateForm = ({ onLogout }) => {
   const [formData, setFormData] = useState({});
   const [error, setError] = useState('');
   const [success, setSuccess] = useState('');
   const [isLoading, setIsLoading] = useState(false);

   const handleInputChange = (e) => {
     setFormData({ ...formData, [e.target.name]: e.target.value });
   };

   const handleSubmit = async (e) => {
     e.preventDefault();
     if (isLoading) return; // Prevent double submission
     
     setError('');
     setSuccess('');
     setIsLoading(true);
     
     try {
       const response = await api.addCertificate(formData);
       setSuccess('Certificate record added successfully!');
       setFormData({}); // Clear form on success
       
       // Show blockchain transaction info if available
       if (response.data.blockchain_tx_hash) {
         setSuccess(prev => prev + ` Blockchain TX: ${response.data.blockchain_tx_hash.substring(0, 10)}...`);
       }
     } catch(err) {
       setError(err.response?.data?.error || err.response?.data?.message || 'An error occurred.');
     } finally {
       setIsLoading(false);
     }
   };

   const inputStyles = "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500";

   return (
      <div className="bg-white p-4 sm:p-8 rounded-lg shadow-lg max-w-2xl mx-auto relative">
        <button onClick={onLogout} className="absolute top-4 right-4 text-sm text-blue-600 hover:underline">Logout</button>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Add New Certificate Record</h2>
         <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700">Student Full Name</label>
                <input type="text" name="student_name" value={formData.student_name || ''} onChange={handleInputChange} className={inputStyles} required />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700">Roll Number / ID</label>
                <input type="text" name="roll_number" value={formData.roll_number || ''} onChange={handleInputChange} className={inputStyles} required />
            </div>
             <div>
                <label className="block text-sm font-medium text-gray-700">Course / Degree Name</label>
                <input type="text" name="course_name" value={formData.course_name || ''} onChange={handleInputChange} className={inputStyles} required />
            </div>
             <div>
                <label className="block text-sm font-medium text-gray-700">Grade / CGPA</label>
                <input type="text" name="grade" value={formData.grade || ''} onChange={handleInputChange} className={inputStyles} required />
            </div>
             <div>
                <label className="block text-sm font-medium text-gray-700">Issue Date</label>
                <input type="date" name="issue_date" value={formData.issue_date || ''} onChange={handleInputChange} className={inputStyles} required />
            </div>
             <div className="md:col-span-2">
                {error && <p className="text-red-500 text-sm">{error}</p>}
                {success && <p className="text-green-500 text-sm">{success}</p>}
                <button 
                  type="submit" 
                  disabled={isLoading}
                  className={`w-full font-bold py-3 px-4 rounded-lg transition-colors ${
                    isLoading 
                      ? 'bg-gray-400 text-gray-200 cursor-not-allowed' 
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {isLoading ? 'Adding Certificate...' : 'Add Record to Database & Blockchain'}
                </button>
             </div>
         </form>
      </div>
   );
};

export default InstitutionPortal;
