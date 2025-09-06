import React, { useState } from 'react';
import { addCertificate } from '../apiService';
import { useAuth } from '../context/AuthContext';

const AddCertificateForm = () => {
   const [formData, setFormData] = useState({
     student_name: '',
     roll_number: '',
     course_name: '',
     grade: '',
     issue_date: ''
   });
   const [error, setError] = useState('');
   const [success, setSuccess] = useState('');
   const [isLoading, setIsLoading] = useState(false);
   const { logout } = useAuth();

   const handleInputChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

   const handleSubmit = async (e) => {
     e.preventDefault();
     setError('');
     setSuccess('');
     setIsLoading(true);
     
     try {
       const response = await addCertificate(formData);
       setSuccess(`Certificate added! TX: ${response.data.blockchain_tx_hash || 'Pending'}`);
       setFormData({
         student_name: '',
         roll_number: '',
         course_name: '',
         grade: '',
         issue_date: ''
       });
     } catch(err) {
       setError(err.response?.data?.error || 'An error occurred.');
     } finally {
       setIsLoading(false);
     }
   };

   const inputStyles = "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors";

   return (
      <div className="card max-w-2xl mx-auto relative">
        <button 
          onClick={logout} 
          className="absolute top-4 right-4 text-sm text-primary-500 hover:text-primary-600 font-medium flex items-center space-x-2"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span>Logout</span>
        </button>
        
        <h2 className="text-2xl font-heading font-bold text-dark mb-6">Add New Certificate Record</h2>
        
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
        
         <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Student Full Name *</label>
                <input 
                  type="text" 
                  name="student_name" 
                  value={formData.student_name} 
                  onChange={handleInputChange} 
                  className={inputStyles} 
                  placeholder="John Doe"
                  required 
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Roll Number / ID *</label>
                <input 
                  type="text" 
                  name="roll_number" 
                  value={formData.roll_number} 
                  onChange={handleInputChange} 
                  className={inputStyles} 
                  placeholder="2021001"
                  required 
                />
            </div>
             <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Course / Degree Name *</label>
                <input 
                  type="text" 
                  name="course_name" 
                  value={formData.course_name} 
                  onChange={handleInputChange} 
                  className={inputStyles} 
                  placeholder="Bachelor of Technology"
                  required 
                />
            </div>
             <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Grade / CGPA *</label>
                <select
                  name="grade"
                  value={formData.grade}
                  onChange={handleInputChange}
                  className={inputStyles}
                  required
                >
                  <option value="">Select Grade</option>
                  <option value="A+">A+</option>
                  <option value="A">A</option>
                  <option value="B+">B+</option>
                  <option value="B">B</option>
                  <option value="C+">C+</option>
                  <option value="C">C</option>
                  <option value="D">D</option>
                  <option value="F">F</option>
                </select>
            </div>
             <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Issue Date *</label>
                <input 
                  type="date" 
                  name="issue_date" 
                  value={formData.issue_date} 
                  onChange={handleInputChange} 
                  className={inputStyles} 
                  required 
                />
            </div>
             <div className="md:col-span-2">
                {/* Info Box */}
                <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-6">
                  <div className="flex items-start space-x-3">
                    <svg className="w-5 h-5 text-primary-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                      <p className="text-sm text-primary-700">
                        <strong>Note:</strong> This will add the certificate record to both the database and the blockchain. 
                        The transaction will be permanently recorded and cannot be modified.
                      </p>
                    </div>
                  </div>
                </div>
                
                <button 
                  type="submit" 
                  disabled={isLoading}
                  className="w-full btn-primary py-3 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Adding to Database & Blockchain...' : 'Add Record to Database & Blockchain'}
                </button>
             </div>
         </form>
      </div>
   );
};

export default AddCertificateForm;

