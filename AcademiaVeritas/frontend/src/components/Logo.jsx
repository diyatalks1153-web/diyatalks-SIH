import React from 'react';

const Logo = ({ size = 'md', showText = true, className = '' }) => {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-20 h-20'
  };

  const textSizeClasses = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl',
    xl: 'text-3xl'
  };

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      {/* Shield Icon with Checkmark */}
      <div className={`${sizeClasses[size]} relative`}>
        <svg
          viewBox="0 0 100 100"
          className="w-full h-full"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Shield Background */}
          <path
            d="M50 5L15 20V50C15 70 30 85 50 95C70 85 85 70 85 50V20L50 5Z"
            fill="#0A74DA"
            className="drop-shadow-lg"
          />
          
          {/* Shield Inner Border */}
          <path
            d="M50 5L15 20V50C15 70 30 85 50 95C70 85 85 70 85 50V20L50 5Z"
            fill="none"
            stroke="#ffffff"
            strokeWidth="2"
            strokeOpacity="0.3"
          />
          
          {/* Checkmark/Tassel */}
          <path
            d="M35 45L42 52L65 30"
            stroke="#18A959"
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="animate-pulse-slow"
            style={{
              strokeDasharray: '30',
              strokeDashoffset: '30',
              animation: 'draw-check 2s ease-in-out forwards'
            }}
          />
          
          {/* Tassel Detail */}
          <circle
            cx="50"
            cy="35"
            r="3"
            fill="#18A959"
            className="animate-bounce-slow"
          />
        </svg>
      </div>
      
      {/* Text */}
      {showText && (
        <span className={`font-heading font-bold text-primary-500 ${textSizeClasses[size]} tracking-tight`}>
          CertiSure
        </span>
      )}
    </div>
  );
};

export default Logo;
