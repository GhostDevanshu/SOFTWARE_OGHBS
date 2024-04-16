import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ShowBookings = () => {
  
  const [bookings, setBookings] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get(process.env.REACT_APP_URI + '/get_all_bookings')
      .then((res) => {
        console.log(res);
        setBookings(res.data.data);
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
      if(response.data.status===0)navigate('/admin');
    else{
    }
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
  }

  return (
    <div className="profile">
      <div>
        <h2>Bookings:</h2>
        {bookings.map((booking, index) => (
          <div key={index} className="blog-preview">
            <div>
              <strong>Booking Status:</strong> {booking.booking_status}
            </div>
            <div>
              <strong>Check-In Date:</strong> {booking.checkindate}
            </div>
            <div>
              <strong>Check-Out Date:</strong> {booking.checkoutdate}
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
            {!(booking.feedback==='')&&(
              <div>
              <strong>Feedback</strong> {booking.feedback}
            </div>
            )}
            <div>
              <strong>Individuals:</strong>
              {booking.individuals.map((individual, indiIndex) => (
                <div key={indiIndex}>
                  <div>Person {indiIndex + 1}:</div>
                  <div>Name: {individual.name}</div>
                  <div>Age, Gender: {individual.age}, {individual.gender}</div>
                  <div>Relation: {individual.relation}</div>
                  <div>Food: {individual.food_option}</div>
                </div>
              ))}
            </div>
            {(booking.booking_status === 'CONFIRMED' || booking.booking_status === 'WAITLISTED') && (
          <button onClick={(e) => handlesubmitbooking(e,booking)}>CANCEL</button>
        )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ShowBookings;
