import React, { useState } from 'react';
import './SignUp.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function SignUp() {
  const navigate = useNavigate();
  const [formsignup, setFormdata] = useState({
    username: '',
    first_name: '',
    last_name: '',
    roll_no: '',
    age: '',
    gender: 'Male',
    address_line_1: '',
    address_line_2: '',
    password: '',
    verify_password: '',
    email: '',
  });
  const [errorMessage, setErrorMessage] = useState('');

  const handlechange = (e) => {
    setFormdata(prevState => ({
      ...prevState,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(formsignup);
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_URI}/register`,
        formsignup,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      console.log('Response data:', response.data);
      if (response.data.status !== 0) {
        setErrorMessage(response.data.message);
      } else {
        navigate('/login');
      }
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
  };

  return (
    <div className="SignApp">
      <div className="Sign-container">
        <h2>SignUp</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" name="username" value={formsignup.username} onChange={handlechange} placeholder="username" required />
          <input type="email" name="email" value={formsignup.email} onChange={handlechange} placeholder="email" required />
          <input type="text" name="roll_no" value={formsignup.roll_no} onChange={handlechange} placeholder="Roll number" required />
          <input type="text" name="first_name" value={formsignup.first_name} onChange={handlechange} placeholder="First name" required />
          <input type="text" name="last_name" value={formsignup.last_name} onChange={handlechange} placeholder="Last name" required />
          <input type="password" name="password" value={formsignup.password} onChange={handlechange} placeholder="Password" required />
          <input type="password" name="verify_password" value={formsignup.verify_password} onChange={handlechange} placeholder="Verify Password" required />
          <input type="text" name="address_line_1" value={formsignup.address_line_1} onChange={handlechange} placeholder="Address Line 1" required />
          <input type="text" name="address_line_2" value={formsignup.address_line_2} onChange={handlechange} placeholder="Address Line 2" required />
          <input type="number" name="age" value={formsignup.age} onChange={handlechange} placeholder="Age" required />
          <div>
            <label>
              <input
                type="radio"
                name="gender"
                value="Male"
                checked={formsignup.gender === 'Male'}
                onChange={handlechange}
              />
              Male
            </label>
            <label>
              <input
                type="radio"
                name="gender"
                value="Female"
                checked={formsignup.gender === 'Female'}
                onChange={handlechange}
              />
              Female
            </label>
            <label>
              <input
                type="radio"
                name="gender"
                value="Other"
                checked={formsignup.gender === 'Other'}
                onChange={handlechange}
              />
              Other
            </label>
          </div>
          <button className="signupbutton" type="submit">SignUp</button>
          <a href="/login">Already SignedUp ??</a>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
        </form>
      </div>
    </div>
  );
}

export default SignUp;
