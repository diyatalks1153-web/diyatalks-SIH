import React from 'react';
import GoogleAuthHandler from './components/GoogleAuthHandler';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import VerifierPage from './pages/VerifierPage';
import PortalPage from './pages/PortalPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-light">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/verify" element={<VerifierPage />} />
          <Route path="/portal" element={<PortalPage />} />
         <Route path="/google-auth-callback" element={<GoogleAuthHandler />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
