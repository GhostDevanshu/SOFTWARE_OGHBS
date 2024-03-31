import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import CheckAvailability from './components/CheckAvailability';
import UserNavbar from './components/UserNavbar';
import Booking from './components/Booking';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <CheckAvailability/>
  </React.StrictMode>
);


