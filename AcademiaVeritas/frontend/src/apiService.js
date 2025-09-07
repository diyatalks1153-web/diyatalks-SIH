import axios from 'axios';

// Create an axios instance with a base URL for our backend
const apiClient = axios.create({
  baseURL: 'http://localhost:5001', // Base URL for all API calls
});

// Use an interceptor to automatically add the JWT token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- API Functions ---
export const verifyCertificate = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/api/verify', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const registerInstitution = (data) => apiClient.post('/api/institution/register', data);
export const loginInstitution = (data) => apiClient.post('/api/institution/login', data);
export const addCertificate = (data) => apiClient.post('/api/certificate/add', data);

export const registerVerifier = (data) => apiClient.post('/api/verifier/register', data);
export const loginVerifier = (data) => apiClient.post('/api/verifier/login', data);

// Default export
export default {
  verifyCertificate,
  registerInstitution,
  loginInstitution,
  addCertificate,
  registerVerifier,
  loginVerifier,
};
