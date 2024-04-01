import React, { useState } from 'react';
import './Home.css';
import { useEffect } from 'react';
import axios from 'axios';

const ForUser = () => {
    const [userinfo,setperson]=useState('')
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
    <div>

      
    <div className="home-container">
      <h1 className="welcome-text">Welcome {userinfo.name} </h1>

    </div>
    <div>
            <a id="book_tickets" href="/signup">BOOK TICKETS</a>
    </div>
    </div >
  );
};

export default ForUser;
