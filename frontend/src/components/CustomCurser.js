import React, { useState, useEffect } from 'react';
import './CustomCurser.css'; // Import CSS file for styling

const CustomCursor = () => {
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });

  // Update cursor position on mouse move
  const handleMouseMove = (event) => {
    setCursorPosition({ x: event.clientX, y: event.clientY });
  };

  useEffect(() => {
    // Add event listener for mouse move
    document.addEventListener('mousemove', handleMouseMove);

    // Cleanup function to remove event listener when component unmounts
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, []); // Empty dependency array ensures the effect runs only once

  return (
    <div
      className="custom-cursor"
      style={{ left: cursorPosition.x, top: cursorPosition.y }}
    ></div>
  );
};

export default CustomCursor;
