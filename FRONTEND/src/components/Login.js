import React, { useState } from 'react';
import './Login.css';
import axios from 'axios';

function Login() {
  const [formlogin, setFormdatalogin] = useState({
    username: '',
    password: ''
  });

  const handlechange = (e) => {
    setFormdatalogin(prevState => ({
      ...prevState,
      [e.target.name]: e.target.value
    }));
  };
  const [showSuccess, setShowSuccess] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(formlogin)
    try {
      const response = await axios({
        method: 'post',
        url: 'http://10.147.133.215:5002/login',
        data: formlogin,
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log('Response data:', response.data);
      if(response.data===100)console.log("user not exist");
      // Handle response data as needed
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
          <input type="text" name="username" value={formlogin.username} onChange={handlechange} placeholder="Username" />
          <input type="password" name="password" value={formlogin.password} onChange={handlechange} placeholder="Password" />
          
          <button className="Loginbutton" type="submit">Login</button>
          <a href="/signup">Don't have an account ?</a>
        </form>
      </div>
    </div>
  );
}

export default Login;
