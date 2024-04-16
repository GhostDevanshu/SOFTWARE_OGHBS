import React from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const PopupMessage = () => {
  const notify = () => {
    toast("Hello! This is a pop-up message.");
  };

  return (
    <div>
      <button onClick={notify}>Show Pop-up</button>
      <ToastContainer />
    </div>
  );
};

export default PopupMessage;
