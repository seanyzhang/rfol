import React from 'react';
import './PageWrapper.css'; 

const PageWrapper = ({
  isExiting,
  children,
}: {
  isExiting: boolean;
  children: React.ReactNode;
}) => {
  return (
    <div className={`page ${isExiting ? 'fade-out' : ''}`}>
      {children}
    </div>
  );
};

export default PageWrapper;