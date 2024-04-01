import React, { useState } from 'react';
import './Payment.css';
import { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
const Payment = () => {
  const [cardNumber, setCardNumber] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [cvv, setCvv] = useState('');
  const [nameOnCard, setNameOnCard] = useState('');
    const navigate=useNavigate();
  const [cost,setcost]=useState('')
  useEffect(() => {
    axios
        .get(process.env.REACT_APP_URI+'/get_payment')
        .then((res) => {
            console.log(res);
            setcost(res.data.data.cost); // Update userinfo with data from API
        })
        .catch((err) => {
            console.error('Error fetching occupancy data:', err);
        });
}, []);
  const handleSubmit = async(event) => {
    event.preventDefault();
    // Handle form submission logic here
    const formpayment={
        card_number:nameOnCard,
        expiry_month:expiryDate,
        cvv:cvv,
        name_on_card:nameOnCard
    }
    console.log(formpayment);
    try {
        const response = await axios({
            method: 'post',
            url: process.env.REACT_APP_URI+'/payment_done',
            data: formpayment,
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        console.log('Response data:', response.data);
        console.log('Response data:', response.data.data);
        console.log('Response data:', response.data.message);
    } catch (error) {
        console.error('Error submitting form data:', error);
    }
    navigate('/profile')
  };

  return (
    <div className="payment-container">
      <h2>Enter Payment Details</h2>
      <h2>Cost={cost}</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Card Number:
          <input
            type="text"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value)}
            required
          />
        </label>
        <label>
          Expiry Date:
          <input
            type="month"
            value={expiryDate}
            onChange={(e) => setExpiryDate(e.target.value)}
            required
          />
        </label>
        <label>
          CVV:
          <input
            type="text"
            value={cvv}
            onChange={(e) => setCvv(e.target.value)}
            required
          />
        </label>
        <label>
          Name on Card:
          <input
            type="text"
            value={nameOnCard}
            onChange={(e) => setNameOnCard(e.target.value)}
            required
          />
        </label>
        <button type="submit">Submit Payment</button>
      </form>
    </div>
  );
};

export default Payment;
