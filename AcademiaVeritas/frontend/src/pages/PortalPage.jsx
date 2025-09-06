import React from 'react';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import AuthForms from '../components/AuthForms';
import AddCertificateForm from '../components/AddCertificateForm';

const PortalPage = () => {
  const { auth } = useAuth();


  return (
    <div className="min-h-screen bg-light">
      <Navbar />
      
      <div className="pt-20 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {auth.token && auth.userType === 'institution' ? (
            // Authenticated institution - show certificate management
            <AddCertificateForm />
          ) : (
            // Not authenticated - show login gate
            <div>
              <div className="text-center mb-8">
                <h1 className="text-3xl font-heading font-bold text-dark mb-4">
                  Institution Portal
                </h1>
                <p className="text-xl text-gray-600">
                  Please log in or register to manage your institution's certificates.
                </p>
              </div>
              <AuthForms userType="institution" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PortalPage;
