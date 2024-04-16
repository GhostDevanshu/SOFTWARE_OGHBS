import { useEffect } from "react";
import axios from "axios";
import { useState } from "react";
const UserNavbar = () => {
  const [userinfo,setperson]=useState({});
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
      <nav className="navbar">
        <h1>Welcome {userinfo.name}  </h1>
        <div className="links">

          <a href="/home">Home</a>
          <a href="/profile">Profile/Bookings</a>
          <a href="/checkavailable">Book Now</a>
          
          <a href="/" style={{ 
            color: 'white', 
            backgroundColor: '#f1356d',
            borderRadius: '8px' 
           }} >LOG OUT</a>
        </div>
      </nav>
    );
  }

  export default UserNavbar;