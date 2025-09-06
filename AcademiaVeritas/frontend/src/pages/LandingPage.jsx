import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Logo from '../components/Logo';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-light">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative pt-16 pb-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-secondary-50">
          <div className="absolute inset-0">
            {/* Animated geometric patterns */}
            <div className="absolute top-20 left-10 w-20 h-20 bg-primary-100 rounded-full opacity-20 animate-pulse-slow"></div>
            <div className="absolute top-40 right-20 w-16 h-16 bg-secondary-100 rounded-full opacity-20 animate-bounce-slow"></div>
            <div className="absolute bottom-20 left-1/4 w-12 h-12 bg-primary-200 rounded-full opacity-30 animate-pulse-slow"></div>
            <div className="absolute bottom-40 right-1/3 w-24 h-24 bg-secondary-200 rounded-full opacity-20 animate-bounce-slow"></div>
          </div>
        </div>
        
        <div className="relative max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-heading font-bold text-dark mb-6 animate-fade-in">
              End Academic Fraud.
              <span className="block text-gradient">Instantly.</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-4xl mx-auto leading-relaxed animate-slide-up">
              CertiSure is an AI and Blockchain-powered platform for instant, immutable verification 
              of academic credentials. Built for the Government of Jharkhand.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center animate-slide-up">
              <Link
                to="/verify"
                className="btn-primary text-lg px-8 py-4 w-full sm:w-auto"
              >
                Verify a Certificate
              </Link>
              <Link
                to="/portal"
                className="btn-secondary text-lg px-8 py-4 w-full sm:w-auto"
              >
                Institution Portal
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* The Problem Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-dark mb-4">
              The Integrity Gap in Academia
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Traditional verification methods are slow, unreliable, and vulnerable to fraud
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="card text-center group hover:shadow-xl transition-all duration-300">
              <div className="w-16 h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-accent-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-heading font-semibold text-dark mb-4">Manual Verification</h3>
              <p className="text-gray-600">
                Takes weeks to verify a single certificate, creating bottlenecks and delays
              </p>
            </div>
            
            <div className="card text-center group hover:shadow-xl transition-all duration-300">
              <div className="w-16 h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-accent-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h3 className="text-xl font-heading font-semibold text-dark mb-4">Vulnerable to Fraud</h3>
              <p className="text-gray-600">
                Easy to forge documents with no immutable verification system
              </p>
            </div>
            
            <div className="card text-center group hover:shadow-xl transition-all duration-300">
              <div className="w-16 h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-accent-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-heading font-semibold text-dark mb-4">Lack of Trust</h3>
              <p className="text-gray-600">
                Employers and institutions struggle to verify credential authenticity
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-light">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-dark mb-4">
              How CertiSure Works
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Simple, secure, and instant verification in four easy steps
            </p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            {[
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                ),
                title: "Upload Document",
                description: "Upload your academic certificate for verification"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                ),
                title: "AI Processing",
                description: "Advanced OCR extracts and validates data"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                ),
                title: "Database Check",
                description: "Cross-reference with institutional records"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                ),
                title: "Blockchain Verify",
                description: "Immutable verification on blockchain"
              }
            ].map((step, index) => (
              <div key={index} className="text-center group">
                <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                  <div className="text-primary-500">
                    {step.icon}
                  </div>
                </div>
                <div className="bg-primary-500 text-white rounded-full w-8 h-8 flex items-center justify-center mx-auto mb-4 font-bold">
                  {index + 1}
                </div>
                <h3 className="text-xl font-heading font-semibold text-dark mb-4">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-dark mb-4">
              An Enterprise-Ready Solution
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built with cutting-edge technology for maximum security and reliability
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                ),
                title: "AI-Powered OCR",
                description: "High-accuracy data extraction from any certificate format"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                ),
                title: "Blockchain Verification",
                description: "Immutable proof of authenticity on Ethereum blockchain"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                ),
                title: "Cloud Integration",
                description: "Scalable cloud infrastructure for high availability"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                ),
                title: "Real-time Dashboard",
                description: "Comprehensive analytics and monitoring tools"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM4.828 7l2.586 2.586a2 2 0 002.828 0L16 7m-5 5a5 5 0 11-10 0 5 5 0 0110 0z" />
                  </svg>
                ),
                title: "Instant Alerts",
                description: "Immediate notifications for verification status"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                ),
                title: "Secure Access",
                description: "Enterprise-grade security and authentication"
              }
            ].map((feature, index) => (
              <div key={index} className="card group hover:shadow-xl transition-all duration-300">
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <div className="text-primary-500">
                    {feature.icon}
                  </div>
                </div>
                <h3 className="text-xl font-heading font-semibold text-dark mb-4">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-light">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-dark mb-4">
              Built with Modern Technology
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Leveraging the latest in AI, blockchain, and web technologies
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-8 items-center">
            {[
              { name: 'Python', color: 'text-blue-500' },
              { name: 'Flask', color: 'text-gray-600' },
              { name: 'React', color: 'text-blue-400' },
              { name: 'PostgreSQL', color: 'text-blue-600' },
              { name: 'Solidity', color: 'text-gray-700' },
              { name: 'Ethereum', color: 'text-purple-500' },
              { name: 'Docker', color: 'text-blue-500' }
            ].map((tech, index) => (
              <div key={index} className="text-center group">
                <div className="w-16 h-16 bg-white rounded-lg shadow-md flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <div className={`text-2xl font-bold ${tech.color}`}>
                    {tech.name.charAt(0)}
                  </div>
                </div>
                <p className="text-sm font-medium text-gray-600">{tech.name}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 gradient-bg">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-heading font-bold text-white mb-6">
            Ready to Transform Academic Verification?
          </h2>
          <p className="text-xl text-white opacity-90 mb-8">
            Join the future of secure, instant credential verification
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link
              to="/verify"
              className="bg-white text-primary-500 hover:bg-gray-50 font-semibold py-4 px-8 rounded-lg transition-all duration-200 transform hover:scale-105"
            >
              Try Verification Now
            </Link>
            <Link
              to="/portal"
              className="border-2 border-white text-white hover:bg-white hover:text-primary-500 font-semibold py-4 px-8 rounded-lg transition-all duration-200 transform hover:scale-105"
            >
              Access Institution Portal
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <Logo size="lg" showText={true} className="text-white" />
              <p className="mt-4 text-gray-300">
                Securing Academic Integrity with AI and Blockchain
              </p>
            </div>
            <div>
              <h3 className="text-lg font-heading font-semibold mb-4">Project</h3>
              <p className="text-gray-300">Smart India Hackathon 2025</p>
              <p className="text-gray-300">Government of Jharkhand</p>
            </div>
            <div>
              <h3 className="text-lg font-heading font-semibold mb-4">Team</h3>
              <p className="text-gray-300">AcademiaVeritas Team</p>
              <p className="text-gray-300">Innovation in Education</p>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 CertiSure. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
