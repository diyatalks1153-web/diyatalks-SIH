import React, { useState, useCallback } from 'react';
import { addCertificate } from '../apiService';
import { useAuth } from '../context/AuthContext';
import { useDropzone } from 'react-dropzone';

const AddCertificateForm = () => {
   const [activeTab, setActiveTab] = useState('manual'); // 'manual' or 'upload'
   const [formData, setFormData] = useState({
     student_name: '',
     roll_number: '',
     course_name: '',
     grade: '',
     issue_date: ''
   });
   const [uploadedFile, setUploadedFile] = useState(null);
   const [filePreview, setFilePreview] = useState(null);
   const [extractedData, setExtractedData] = useState(null);
   const [error, setError] = useState('');
   const [success, setSuccess] = useState('');
   const [isLoading, setIsLoading] = useState(false);
   const [isProcessing, setIsProcessing] = useState(false);
   const { logout } = useAuth();

   const handleInputChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

   // Handle manual form submission
   const handleManualSubmit = async (e) => {
     e.preventDefault();
     setError('');
     setSuccess('');
     setIsLoading(true);
     
     try {
       const response = await addCertificate(formData);
       setSuccess(`Certificate added successfully! TX: ${response.data.blockchain_tx_hash || 'Pending'}`);
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

   // Handle file upload and processing
   const onDrop = useCallback(async (acceptedFiles) => {
     const file = acceptedFiles[0];
     if (!file) return;

     // Validate file type
     if (!['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'].includes(file.type)) {
       setError('Please upload a valid image (JPG, PNG) or PDF file.');
       return;
     }

     setUploadedFile(file);
     setError('');
     setIsProcessing(true);

     // Create file preview
     const reader = new FileReader();
     reader.onload = (e) => setFilePreview(e.target.result);
     reader.readAsDataURL(file);

     try {
       // Send file to backend for OCR processing
       const formDataToSend = new FormData();
       formDataToSend.append('file', file);
       formDataToSend.append('extract_only', 'true'); // Flag to only extract data, not add certificate
       
       const response = await fetch('http://localhost:5001/api/certificate/extract', {
         method: 'POST',
         headers: {
           'Authorization': `Bearer ${localStorage.getItem('authToken')}`
         },
         body: formDataToSend
       });

       const result = await response.json();

       if (response.ok) {
         setExtractedData(result.extracted_data);
         // Pre-fill the form with extracted data
         setFormData({
           student_name: result.extracted_data.student_name || '',
           roll_number: result.extracted_data.roll_number || '',
           course_name: result.extracted_data.course_name || '',
           grade: result.extracted_data.grade || '',
           issue_date: result.extracted_data.issue_date || ''
         });
       } else {
         setError(result.error || 'Failed to extract data from certificate');
       }
     } catch (err) {
       setError('Error processing uploaded file');
       console.error('File processing error:', err);
     } finally {
       setIsProcessing(false);
     }
   }, []);

   // Handle upload-based submission
   const handleUploadSubmit = async (e) => {
     e.preventDefault();
     if (!uploadedFile) {
       setError('Please upload a certificate file first.');
       return;
     }

     setError('');
     setSuccess('');
     setIsLoading(true);
     
     try {
       // Submit the final data (either extracted or manually corrected)
       const response = await addCertificate(formData);
       setSuccess(`Certificate added successfully! TX: ${response.data.blockchain_tx_hash || 'Pending'}`);
       
       // Clear form and reset upload state
       setFormData({
         student_name: '',
         roll_number: '',
         course_name: '',
         grade: '',
         issue_date: ''
       });
       setUploadedFile(null);
       setFilePreview(null);
       setExtractedData(null);
     } catch(err) {
       setError(err.response?.data?.error || 'An error occurred.');
     } finally {
       setIsLoading(false);
     }
   };

   // Clear upload data
   const clearUpload = () => {
     setUploadedFile(null);
     setFilePreview(null);
     setExtractedData(null);
     setFormData({
       student_name: '',
       roll_number: '',
       course_name: '',
       grade: '',
       issue_date: ''
     });
   };

   const inputStyles = "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors";
   
   const { getRootProps, getInputProps, isDragActive } = useDropzone({
     onDrop,
     accept: {
       'image/*': ['.jpeg', '.jpg', '.png'],
       'application/pdf': ['.pdf']
     },
     multiple: false,
     disabled: isProcessing
   });

   return (
      <div className="card max-w-4xl mx-auto relative">
        <button 
          onClick={logout} 
          className="absolute top-4 right-4 text-sm text-primary-500 hover:text-primary-600 font-medium flex items-center space-x-2 z-10"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span>Logout</span>
        </button>
        
        <h2 className="text-2xl font-heading font-bold text-dark mb-6">Add New Certificate Record</h2>
        
        {/* Tab Navigation */}
        <div className="flex mb-6 bg-gray-100 rounded-lg p-1">
          <button 
            onClick={() => setActiveTab('manual')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'manual' 
                ? 'bg-white text-primary-600 shadow-sm' 
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Manual Entry
          </button>
          <button 
            onClick={() => setActiveTab('upload')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'upload' 
                ? 'bg-white text-primary-600 shadow-sm' 
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            Upload Certificate
          </button>
        </div>
        
        {/* Message Display */}
        {error && (
          <div className="mb-6 p-4 rounded-lg bg-red-50 text-red-700 border border-red-200">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {error}
            </div>
          </div>
        )}
        {success && (
          <div className="mb-6 p-4 rounded-lg bg-green-50 text-green-700 border border-green-200">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {success}
            </div>
          </div>
        )}
        
        {activeTab === 'manual' ? (
         /* Manual Entry Tab */
         <form onSubmit={handleManualSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
        ) : (
         /* Upload Certificate Tab */
         <div className="space-y-6">
           {!uploadedFile ? (
             /* Drag & Drop Area */
             <div 
               {...getRootProps()} 
               className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                 isDragActive 
                   ? 'border-primary-500 bg-primary-50' 
                   : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
               } ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
             >
               <input {...getInputProps()} />
               <div className="space-y-4">
                 <div className="flex justify-center">
                   <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                   </svg>
                 </div>
                 <div>
                   <p className="text-lg font-medium text-gray-900">
                     {isDragActive ? 'Drop your certificate here...' : 'Upload Certificate Image or PDF'}
                   </p>
                   <p className="text-sm text-gray-500 mt-2">
                     {isProcessing ? 'Processing...' : 'Drag & drop or click to select • JPG, PNG, PDF up to 10MB'}
                   </p>
                 </div>
                 {isProcessing && (
                   <div className="flex justify-center">
                     <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
                   </div>
                 )}
               </div>
             </div>
           ) : (
             /* File Preview & Extracted Data */
             <div className="space-y-6">
               <div className="bg-gray-50 rounded-lg p-6">
                 <div className="flex items-center justify-between mb-4">
                   <h3 className="text-lg font-medium text-gray-900">Uploaded Certificate</h3>
                   <button
                     onClick={clearUpload}
                     className="text-sm text-red-600 hover:text-red-700 font-medium"
                   >
                     Clear Upload
                   </button>
                 </div>
                 
                 {filePreview && (
                   <div className="mb-4">
                     {uploadedFile.type === 'application/pdf' ? (
                       <div className="bg-white border-2 border-gray-200 rounded-lg p-4 text-center">
                         <svg className="w-12 h-12 text-red-500 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                           <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                         </svg>
                         <p className="text-sm text-gray-600">{uploadedFile.name}</p>
                       </div>
                     ) : (
                       <img 
                         src={filePreview} 
                         alt="Certificate preview" 
                         className="w-full max-w-md mx-auto rounded-lg shadow-md"
                       />
                     )}
                   </div>
                 )}
                 
                 {extractedData && (
                   <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                     <h4 className="text-sm font-medium text-blue-900 mb-2">Extracted Information:</h4>
                     <div className="grid grid-cols-2 gap-2 text-sm">
                       <div><strong>Student:</strong> {extractedData.student_name || 'Not detected'}</div>
                       <div><strong>Roll No:</strong> {extractedData.roll_number || 'Not detected'}</div>
                       <div><strong>Course:</strong> {extractedData.course_name || 'Not detected'}</div>
                       <div><strong>Grade:</strong> {extractedData.grade || 'Not detected'}</div>
                       <div className="col-span-2"><strong>Date:</strong> {extractedData.issue_date || 'Not detected'}</div>
                     </div>
                   </div>
                 )}
               </div>
               
               {/* Editable Form */}
               <form onSubmit={handleUploadSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                 <div className="md:col-span-2">
                   <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                     <p className="text-sm text-yellow-800">
                       <strong>Review & Edit:</strong> Please verify and correct the extracted information below before submitting.
                     </p>
                   </div>
                 </div>
                 
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
                     <button 
                       type="submit" 
                       disabled={isLoading}
                       className="w-full btn-primary py-3 disabled:opacity-50 disabled:cursor-not-allowed"
                     >
                       {isLoading ? 'Adding to Database & Blockchain...' : 'Add Extracted Certificate to Database & Blockchain'}
                     </button>
                 </div>
               </form>
             </div>
           )}
         </div>
        )}
      </div>
   );
};

export default AddCertificateForm;

