import React, { useState } from 'react';
import './Booking.css';
import axios from 'axios';
function Booking() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [numberOfPeople, setNumberOfPeople] = useState('');
  const [names, setNames] = useState([]);

  const handleNameChange = (index, value) => {
    const newNames = [...names];
    newNames[index] = value;
    setNames(newNames);
  };

  const handleSubmit = async(event) => {
    event.preventDefault();
  
    // Construct the data object to send to the backend
    const bookingData = {
      startDate: startDate,
      endDate: endDate,
      numberOfPeople: numberOfPeople,
      names: {}
    };
  
    // Convert array of names to dictionary
    names.forEach((name, index) => {
      bookingData.names[index + 1] = name; // Use index + 1 as key to start from 1
    });
  
    console.log(bookingData);
    try {
        const response = await axios({
          method: 'post',
          url: process.env.REACT_APP_URI+'/book',
          data: bookingData,
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        console.log('Response data:', response.data);
        console.log('Response data:', response.data.data);
        console.log('Response data:', response.data.message);
      } catch (error) {
        console.error('Error submitting form data:', error);
        // Add error handling here, like displaying an error message to the user
      }
    // Send the bookingData to the backend
    // For testing, you can replace this with actual API call
  };
  

  const handleNumberOfPeopleChange = (event) => {
    const newNumberOfPeople = event.target.value;
    setNumberOfPeople(newNumberOfPeople);
    const newNames = newNumberOfPeople > names.length ? [...names, ...Array(newNumberOfPeople - names.length).fill('')] : names.slice(0, newNumberOfPeople);
    setNames(newNames);
  };

  return (
    <div className="booking-container">
      <form onSubmit={handleSubmit} className="booking-form">
        <label className="booking-label">
          Start Date:
          <input 
            type="date" 
            value={startDate} 
            onChange={(event) => setStartDate(event.target.value)} 
            required 
            className="booking-input"
          />
        </label>
        <label className="booking-label">
          End Date:
          <input 
            type="date" 
            value={endDate} 
            onChange={(event) => setEndDate(event.target.value)} 
            required 
            className="booking-input"
          />
        </label>
        <label className="booking-label">
          Number of People:
          <input 
            type="number" 
            value={numberOfPeople} 
            onChange={handleNumberOfPeopleChange} 
            required 
            className="booking-input"
          />
        </label>
        <h3>Names of People:</h3>
        {names.map((name, index) => (
          <div key={index}>
            <input
              type="text"
              value={name}
              onChange={(event) => handleNameChange(index, event.target.value)}
              required
              className="booking-input"
            />
          </div>
        ))}
        <br />
        <button type="submit" className="submit-button">Submit</button>
      </form>
    </div>
  );
}

export default Booking;
