import React from 'react';

const LoadingSpinner = ({ size = 'md', text = '', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  };

  return (
    <div className={`flex items-center justify-center space-x-3 ${className}`}>
      <div className={`animate-spin rounded-full border-2 border-gray-300 border-t-primary-500 ${sizeClasses[size]}`}></div>
      {text && <span className="text-gray-600 font-medium">{text}</span>}
    </div>
  );
};

export default LoadingSpinner;
