import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import Logo from './Logo';

const Navbar = () => {
  const location = useLocation();
  const isLandingPage = location.pathname === '/';

  return (
    <nav className="bg-white shadow-md w-full fixed top-0 left-0 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo Section */}
          <Link to="/" className="flex-shrink-0 flex items-center hover:opacity-80 transition-opacity">
            <Logo size="md" showText={true} />
          </Link>

          {/* Navigation - Only show on sub-pages */}
          {!isLandingPage && (
            <div className="flex items-center">
              <Link
                to="/"
                className="text-primary-500 hover:text-primary-600 font-medium transition-colors duration-200 flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                <span>Back to Home</span>
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
