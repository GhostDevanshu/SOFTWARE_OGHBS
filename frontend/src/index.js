import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Home from './components/Home';
import App from './App';
import CheckAvailability from './components/CheckAvailability';
import UserNavbar from './components/UserNavbar';
import Booking from './components/Booking';
import Payment from './Payment';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App/>
  </React.StrictMode>
);


