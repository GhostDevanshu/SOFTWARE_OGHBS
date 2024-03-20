// App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const toggleLogin = () => {
    setIsLogin(!isLogin);
  };

  const handlesubmit = (e) => {
    e.preventDefault();

    // Perform login or signup action
    if (isLogin) console.log({ username, password });
    else console.log({ username, email, password });
  };

  const handlepassword = (e) => {
    setPassword(e.target.value);
  };

  const handleUsername = (e) => {
    setUsername(e.target.value);
  };

  const handleEmail = (e) => {
    setEmail(e.target.value);
  };

  return (
    <div className="App">
      <div className="login-container">
        <h2>{isLogin ? 'Login' : 'Sign Up'}</h2>
        <form onSubmit={handlesubmit}>
          {!isLogin && (
            <input
              type="email"
              placeholder="Email"
              onChange={handleEmail}
              value={email}
            />
          )}
          <input
            type="text"
            placeholder="username"
            onChange={handleUsername}
            value={username}
          />
          <div className="password-input">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              onChange={handlepassword}
              value={password}
            />
            <label htmlFor="showPassword">
              <input
                type="checkbox"
                id="showPassword"
                checked={showPassword}
                onChange={() => setShowPassword(!showPassword)}
              />
              Show Password
            </label>
          </div>
          <button type="submit">{isLogin ? 'Login' : 'Sign Up'}</button>
        </form>
        <p onClick={toggleLogin} className="toggle-login">
          {isLogin ? "Don't have an account? Sign Up" : 'Already have an account? Login'}
        </p>
      </div>
      
    </div>
  );
}

export default App;
