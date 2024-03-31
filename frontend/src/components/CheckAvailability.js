import React, { useState } from 'react';
import './CheckAvailability.css';
import axios from 'axios';

function CheckAvailability() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedGuestHouse, setSelectedGuestHouse] = useState('');
  const [isok,setok]=useState(false);
  const [responseafter,setresponse]=useState([])
  const handleSubmit = async(event) => {
    event.preventDefault();

    // Construct the data object to send to the backend
    const formData = {
      checkindate: startDate,
      checkoutdate: endDate,
      guest_house: selectedGuestHouse // Include selected guest house in formData
    };
    console.log(formData);
    try {
        const response = await axios({
          method: 'post',
          url: process.env.REACT_APP_URI+'/checkavailable',
          data: formData,
          headers: { 'Content-Type': 'multipart/form-data' },

        });
        console.log('Response data:', response.data);
        console.log('Response data:', response.data.data);
        console.log('Response data:', response.data.message);
        console.log(typeof(response.data))
        setresponse(response.data.rooms)
        setok(true);
      } catch (error) {
        console.error('Error submitting form data:', error);
        // Add error handling here, like displaying an error message to the user
      }

      console.log("response after "+{responseafter})
    // Send the formData to the backend, you can use fetch or axios for this
  };

  return (
    <div className="date-form-container">
      <form onSubmit={handleSubmit} className="date-form">
        <label className="date-label">
          Start Date:
          <input 
            type="date" 
            value={startDate} 
            onChange={(event) => setStartDate(event.target.value)} 
            required 
            className="date-input"
          />
        </label>
        <label className="date-label">
          End Date:
          <input 
            type="date" 
            value={endDate} 
            onChange={(event) => setEndDate(event.target.value)} 
            required 
            className="date-input"
          />
        </label>
        <label className="date-label">
          Guest House:
          <select
            value={selectedGuestHouse}
            onChange={(event) => setSelectedGuestHouse(event.target.value)}
            className="guest-house-select"
            required
          >
            <option value="">Select Guest House</option>
            <option value="TGH">Guest House 1</option>
            <option value="VGH">Guest House 2</option>
            <option value="KGH">Guest House 3</option>
          </select>
        </label>
        <button type="submit" className="submit-button">Submit</button>
      </form>
      {isok&&(
        <div>
            {responseafter.map((each)=>(
               <div key={each.floor}>
                <h5>{each.code}</h5>
               </div>
            ))}
        </div>
      ) }
     
    </div>
  );
}

export default CheckAvailability;
