import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const AllUsers = () => {
  const [persons, setPersons] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_URI}/get_all_users`)
      .then((res) => {
        console.log(res);
        setPersons(res.data.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  const handleVerifyByAdmin = async (event, info) => {
    event.preventDefault();
    const formForVerify = {
      user_id: info._id,
    };
    try {
        const response = await axios({
            method: 'post',
            url: process.env.REACT_APP_URI + '/verify_user',
            data: formForVerify, // Use formAfterBook instead of formAfterBooking
            headers: { 'Content-Type': 'multipart/form-data' },
          });
      console.log(response);
      navigate("/admin");
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
  };

  const handleKickByAdmin = async (event, info) => {
    event.preventDefault();
    const formForKick = {
      user_id: info._id,
    };
    try {
        const response = await axios({
            method: 'post',
            url: process.env.REACT_APP_URI + '/kick_user',
            data: formForKick, // Use formAfterBook instead of formAfterBooking
            headers: { 'Content-Type': 'multipart/form-data' },
          });
      console.log(response);
      navigate("/admin");
    } catch (error) {
      console.error('Error submitting form data:', error);
      // Add error handling here, like displaying an error message to the user
    }
  };

  return (
    <div className="blog-preview">
  <h2>List of Persons:</h2>
  <div>
    {persons.length > 0 ? (
      persons.map((each, index) => (
        <div key={index} className="person-info">
          <div>
            <div>Name: {each.name}</div>
            <div>Age: {each.age}</div>
            <div>Roll Number: {each.roll_no}</div>
            <div>Status: {each.verified}</div>
          </div>
          <div className="actions">
            {!(each.verified === "VERIFIED") && (
              <button onClick={(e) => handleVerifyByAdmin(e, each)}>Verify</button>
            )}
            <button onClick={(e) => handleKickByAdmin(e, each)} >Kick out</button>
          </div>
        </div>
      ))
    ) : (
      <p>Loading...</p>
    )}
  </div>
</div>

  );
};

export default AllUsers;
