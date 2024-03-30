import React, { createContext, useContext, useState } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [info, setInfo] = useState({
    first_name: "abcd",
    last_name: "abcd@abc",
    race: "abcd"
  });

  const [loginResponse, setLoginResponse] = useState(null); // New state for login response

  return (
    <UserContext.Provider value={{ info, setInfo, loginResponse, setLoginResponse }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);
