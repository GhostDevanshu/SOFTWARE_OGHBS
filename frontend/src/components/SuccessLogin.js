import React from 'react';
import './SuccessLogin.css'; // Import CSS file for styling

const SuccessLogin = ({userinfoafterlogin}) => {
  console.log(userinfoafterlogin)
  return (
    <div className="success-login">
      <h2>{userinfoafterlogin.first_name}</h2>
      <h2>{userinfoafterlogin.last_name}</h2>
      <h2>you are  {userinfoafterlogin.race}</h2>
    </div>
  );
};

export default SuccessLogin;
