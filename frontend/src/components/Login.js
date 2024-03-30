import React, { useState } from 'react';
import './Login.css';
import axios from 'axios';
import Profile from './Profile';
import { useNavigate } from 'react-router-dom';
import UserNavbar from '../UserNavbar';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
function Login() {
  
  const info = {
    first_name:"abcd",
    last_name:"abcd@abc",
    race:"abcd"
  }
  const navigate=useNavigate();
  const [formlogin, setFormdatalogin] = useState({
    username: '',
    password: '',
  });

  const handlechange = (e) => {
    setFormdatalogin(prevState => ({
      ...prevState,
      [e.target.name]: e.target.value
    }));
  }
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(formlogin)
    try {
      const response = await axios({
        method: 'post',
        url: 'http://10.145.215.252:5002/login',
        data: formlogin,
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log('Response data:', response.data);
      console.log('Response data:', response.data.data);
      console.log('Response data:', response.data.message);
      if(response.data.status===0){
        navigate('/profile')
        console.log("dnfoosf")
      }
      // Handle response data as needed
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
    formlogin.iscorrect=true;
    console.log("helloooooo")
  }
  
  return (
   
    (<div className="LoginApp">
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" name="username" value={formlogin.username} onChange={handlechange} placeholder="Username" />
          <input type="password" name="password" value={formlogin.password} onChange={handlechange} placeholder="Password" />
          
          <button className="Loginbutton" type="submit">Login</button>
          <a href="/signup">Don't have an account ?</a>
        </form>
      </div>
    </div>)
  );
}

export default Login;
