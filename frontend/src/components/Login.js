import React, { useState } from 'react';
import './Login.css';
import axios from 'axios';
import Profile from './Profile';
import { useNavigate } from 'react-router-dom';
import UserNavbar from './UserNavbar';

function Login() {
  const navigate = useNavigate();
  const [formlogin, setFormdatalogin] = useState({
    username: '',
    password: '',
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [popupMessage, setPopupMessage] = useState('');

  const handlechange = (e) => {
    setFormdatalogin((prevState) => ({
      ...prevState,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await axios({
        method: 'post',
        url: process.env.REACT_APP_URI+'/login',
        data: formlogin,
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      console.log('Response data:', response.data);
      console.log('Response data:', response.data.data);
      console.log('Response data:', response.data.message);
      
      setPopupMessage(response.data.message);
      setShowPopup(true);

      if (response.data.status === 0) {
        alert(response.data.message)
        navigate('/home');
        console.log('dnfoosf');
      } 
      else if(response.data.status===1000){
        alert("Admin Login")
        navigate('/admin')
      }
      else {
        alert(response.data.message)
        setErrorMessage('Incorrect credentials. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
  };

  return (
    <div className="LoginApp">
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            value={formlogin.username}
            onChange={handlechange}
            placeholder="Username"
            required
          />
          <input
            type="password"
            name="password"
            value={formlogin.password}
            onChange={handlechange}
            placeholder="Password"
            required
          />
          <button className="Loginbutton" type="submit">
            Login
          </button>
          <a href="/signup">Don't have an account ?</a>
        </form>
        {showPopup && (
          <div className="popup">
            <div className="popup-content">
              <p>{popupMessage}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Login;
