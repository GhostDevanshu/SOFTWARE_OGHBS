import React from 'react';
import './Home.css';
import CustomCursor from './CustomCurser';
const Home = () => {
  return (
    <div>
      <CustomCursor></CustomCursor>
      
    <div className="home-container">
      <h1 className="welcome-text">Welcome to IIT KGP Guest House </h1>

    </div>
    <div>
            <a id="book_tickets" href="/signup">BOOK TICKETS</a>
    </div>
    </div >
  );
};

export default Home;
