import React, { useState } from 'react';
import './CheckAvailability.css';
import axios from 'axios';
import CheckAvailabilitycard from './Checkavailabilitycard';
import { useNavigate } from 'react-router-dom';
function CheckAvailability() {
    const navigate=useNavigate()
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedGuestHouse, setSelectedGuestHouse] = useState('');
  const [isok,setok]=useState(false);
  const [responseafter,setresponse]=useState([])
  const [isbook,setbook]=useState(false)
  
//   setFormdatalogin((prevState) => ({
//     ...prevState,
//     [e.target.name]: e.target.value,
//   }));
const handlesubmitbooking = async(event,info) => {
    event.preventDefault()
    const formAfterBook={
        checkindate: startDate,
          checkoutdate: endDate,
          guest_house: selectedGuestHouse,
          room_code: info.code,
         available: info.available,
         occupancy:info.Occupancy,
    }
    console.log(startDate)
    console.log(endDate)
    console.log(info.code)
    console.log(selectedGuestHouse)
    console.log(info.available)
  
    console.log(formAfterBook); // This will log the updated state
  
    try {
      const response = await axios({
        method: 'post',
        url: process.env.REACT_APP_URI + '/initiatebooking',
        data: formAfterBook, // Use formAfterBook instead of formAfterBooking
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      navigate('/book');
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
  };
  

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
        console.log(response.data.data.rooms)

        setresponse(response.data.data.rooms)
        setok(true);
      } catch (error) {
        console.error('Error submitting form data:', error);
        // Add error handling here, like displaying an error message to the user
      }

      console.log("response after "+{responseafter})
    // Send the formData to the backend, you can use fetch or axios for this
  };

  return (
    <div className="date-form-container" >
      {!isok&&(<form onSubmit={handleSubmit} className="date-form">
        <h4>Availability</h4>
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
            <option value="TGH">TGH</option>
            <option value="VGH">VGH</option>
            <option value="KGH">KGH</option>
          </select>
        </label>
        <button type="submit" className="submit-button">Submit</button>
      </form>)}
      {isok&&(
        <div>
            <p>AVAILABILITY</p>
            {responseafter.map((each,index)=>(
               <div key={index} className="blog-preview">
                <CheckAvailabilitycard/>
                <h1>{each.description}</h1>
                <h2>Air-Conditioned={each.AC} ,Availability={each.available},Floor={each.floor} </h2>
                <h2>Price=Rs{each.price_per_day}/- per day </h2>
                <h2>No Of persons per room={each.Occupancy}</h2>

                <button onClick={(e)=>handlesubmitbooking(e,each)}>BOOK</button>
                {each.trying&&(<div>
                    <h1>hello</h1>
                </div>)}
               </div>
            ))}
        </div>
      ) }
    </div>
  );
}

export default CheckAvailability;
