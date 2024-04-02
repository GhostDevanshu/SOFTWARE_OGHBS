import React, { useState } from 'react';
import { useEffect } from 'react';
import axios from 'axios';
const Profile = ({}) => {

const [person,setperson]=useState({});
useEffect(() => {
  axios
    .get(process.env.REACT_APP_URI+'/profile')
    .then((res) => {
      console.log(res);
      setperson(res.data.data)
    })
    .catch((err) => {
    });
}, []);
  return (
    <div className="profile">
      <h1>Profile</h1>
      <div>
        <strong>Name:</strong> {person.name}
      </div>
      <div>
        <strong>Email:</strong> {person.gender}
      </div>
      <div>
        <strong>Age:</strong> {person.age}
      </div>
      {/* Add more details as needed */}
      
    </div>
  );
};

export default Profile;
