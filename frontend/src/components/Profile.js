import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Profile.css'

const Profile = () => {
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [person, setPerson] = useState({});
const navigate=useNavigate()

  useEffect(() => {
    axios
      .get(process.env.REACT_APP_URI + '/profile')
      .then((res) => {
        console.log(res);
        setPerson(res.data.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);
  const handlesubmitbooking = async(event,info) => {
    event.preventDefault()
    const formAftercancel={
    booking_id:info._id
    }

    console.log(formAftercancel); // This will log the updated state
    try {
      const response = await axios({
        method: 'post',
        url: process.env.REACT_APP_URI + '/cancellation',
        data: formAftercancel, // Use formAfterBook instead of formAfterBooking
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      console.log(response)
      if(response.data.status===0)navigate('/home');
    else{
    }
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
  };
  const handlesubmitfeedback=async(event,info)=>{
    event.preventDefault()
    const formAfterfeedback={
    booking_id:info._id,
      feedback:feedback
    }
    
    
    console.log(formAfterfeedback); // This will log the updated state
  
    try {
      const response = await axios({
        method: 'post',
        url: process.env.REACT_APP_URI + '/feedback',
        data: formAfterfeedback, // Use formAfterBook instead of formAfterBooking
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      console.log(response)
      if(response.data.status===0)navigate('/home');
    else{
    }
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
  }
  return (
    <div >
      <div className='profile'>
      <h1>Profile</h1>
      <div>
        <strong>Name:</strong> {person.name}
      </div>
      <div>
        <strong>Email:</strong> {person.email}
      </div>
      <div>
        <strong>Age:</strong> {person.age}
      </div>
      </div>
      <div>
        <h2>Bookings:</h2>
        {person.bookings &&
          person.bookings.map((booking, index) => (
            <div key={index} className="blog-preview">
              <div>
                <strong>Booking Status:</strong> {booking.booking_status}
              </div>
              <div>
                <strong>CheckIn data:</strong> {booking.checkindate}
              </div>
              <div>
                <strong>CheckOut data:</strong> {booking.checkoutdate}
              </div>
              <div>
                <strong>Guest House:</strong> {booking.guest_house}
              </div>
              <div>
                <strong>Payement Status:</strong> {booking.payment_status}
              </div>
              <div>
                <strong>Room Code:</strong> {booking.room_code}
              </div>
              <div>
                <strong>Amount Paid:</strong> {booking.cost}
              </div>

              <div>INDIVIDUALS:</div>
              {booking.individuals && // Corrected this line
                booking.individuals.map((indi, indiIndex) => ( // Changed index to indiIndex
                  <div key={indiIndex}>
                    
                    <div>Person {indiIndex+1}:</div>

                    <div>
                      <div> Name={indi.name}</div>
                    </div>
                    <div>
                      <div> Age,Gender={indi.age},{indi.gender}</div>
                    </div>
                    <div>
                      <div> Relation={indi.relation}</div>
                    </div>
                  </div>
                ))}
            {(booking.booking_status === 'CONFIRMED' || booking.booking_status === 'WAITLISTED') && (
          <button onClick={(e) => handlesubmitbooking(e,booking)}>CANCEL</button>
        )}
          {(booking.booking_status==="COMPLETED")&&(<button onClick={() => setShowFeedbackForm(true)}>Feedback</button>)}
      {showFeedbackForm && (booking.booking_status==="COMPLETED") && (
        <div>
          <h2>Feedback</h2>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="Enter your feedback here..."
            rows={4}
            cols={50}
          />
          <button onClick={(e)=>handlesubmitfeedback(e,booking)}>Submit</button>
        </div>
      )}
            </div>
        ))}
      </div>
    </div>
  );
};

export default Profile;
{/* <button onClick={(e)=>handlesubmitbooking(e,each)}>BOOK</button> */}