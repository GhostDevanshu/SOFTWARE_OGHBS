import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Booking.css';
import { useNavigate } from 'react-router-dom';
function Booking() {
    const [userinfo, setUserInfo] = useState({ occupancy: 0 }); // Initialize userinfo with default occupancy value of 0
    const [numberOfPeople, setNumberOfPeople] = useState(0); // Initialize numberOfPeople with 0
    const [peopleInfo, setPeopleInfo] = useState([]);
    const navigate=useNavigate();
    useEffect(() => {
        axios
            .get(process.env.REACT_APP_URI+'/getoccupancy')
            .then((res) => {
                console.log(res);
                setUserInfo(res.data.data); // Update userinfo with data from API
            })
            .catch((err) => {
                console.error('Error fetching occupancy data:', err);
            });
    }, []);

    useEffect(() => {
        // Update numberOfPeople state when userinfo changes
        setNumberOfPeople(userinfo.occupancy);
        const updatedPeopleInfo = [];
        for (let i = 0; i < numberOfPeople; i++) {
            updatedPeopleInfo.push({
                name: '',
                gender: '',
                age: '',
                relation: '',
                food:''
            });
        }
        setPeopleInfo(updatedPeopleInfo);
    }, [userinfo]);

    const handleInfoChange = (index, field, value) => {
        const updatedPeopleInfo = [...peopleInfo];
        updatedPeopleInfo[index][field] = value;
        setPeopleInfo(updatedPeopleInfo);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const bookingData = {
            numberOfPeople: numberOfPeople,
            peopleInfo: peopleInfo
        };

        console.log(bookingData);
        try {
            const response = await axios({
                method: 'post',
                url: process.env.REACT_APP_URI+'/addingindividual',
                data: bookingData,
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            console.log('Response data:', response.data);
            console.log('Response data:', response.data.data);
            console.log('Response data:', response.data.message);
        } catch (error) {
            console.error('Error submitting form data:', error);
        }
        navigate('/getpayment')
    };


    return (
        <div className="booking-container">
            <form onSubmit={handleSubmit} className="booking-form">
                <label className="booking-label">
                    Number of People: {userinfo.occupancy}
                </label>
                <div className="people-info-container">
                    {numberOfPeople && Array.from({ length: numberOfPeople }).map((_, index) => (
                        <div key={index} className="person-info">
                            <h3>Person {index + 1}</h3>
                            <label className="booking-label">
                                <input
                                    placeholder='Name'
                                    type="text"
                                    value={peopleInfo[index]?.name || ''}
                                    onChange={(event) => handleInfoChange(index, 'name', event.target.value)}
                                    required
                                    className="booking-input"
                                />
                            </label>
                            <div className="booking-radio-group">
    <label className="booking-radio-label">
        <input
            type="radio"
            name={`gender-${index}`}
            value="Male"
            checked={peopleInfo[index]?.gender === 'Male'}
            onChange={(event) => handleInfoChange(index, 'gender', event.target.value)}
            className="booking-radio-input"
        />
        Male
    </label>
    <label className="booking-radio-label">
        <input
            type="radio"
            name={`gender-${index}`}
            value="Female"
            checked={peopleInfo[index]?.gender === 'Female'}
            onChange={(event) => handleInfoChange(index, 'gender', event.target.value)}
            className="booking-radio-input"
        />
        Female
    </label>
</div>
                            <label className="booking-label">
                                <input
                                    placeholder='Age'
                                    type="number"
                                    value={peopleInfo[index]?.age || ''}
                                    onChange={(event) => handleInfoChange(index, 'age', event.target.value)}
                                    required
                                    className="booking-input"
                                />
                            </label>
                            <label className="booking-label">
                                <input
                                    placeholder='Relation'
                                    type="text"
                                    value={peopleInfo[index]?.relation || ''}
                                    onChange={(event) => handleInfoChange(index, 'relation', event.target.value)}
                                    required
                                    className="booking-input"
                                />
                            </label>
                            <label className="date-label">
          Food:
          <select
            value={peopleInfo[index]?.food||''}
            onChange={(event) => handleInfoChange(index,'food',event.target.value)}
            required
          >
            <option value="">Food Options</option>
            <option value="Veg food (single person)">Veg food (single person) price =Rs.200/- </option>
            <option value="Non Veg Food (single person)">Non Veg food (single person) price=Rs.200/-</option>
            <option value="No food required">No food required</option>
          </select>
        </label>    
                        </div>
                    ))}
                </div>
                <br />
                <button type="submit" className="submit-button">Submit</button>
            </form>
        </div>
    );
}

export default Booking;
