// App.js
import React from 'react';
import './App.css';
import Home from './components/Home';
import Login from './components/Login';
import SignUp from './components/SignUp';
import Navbar from './components/Navbar';
import SuccessLogin from './components/SuccessLogin';
import {  createBrowserRouter,RouterProvider } from "react-router-dom";
import About from './components/About';
import Profile from './components/Profile';
import UserNavbar from './UserNavbar';
import { useUser } from './components/context';
function App() {
  
  // const {info} =useUser();
  const info = {
    first_name:"abc",
    last_name:"abc@abc",
    race:"abc"
  }
  const router =createBrowserRouter([
    
   {
    path: '/',
    element :<div><Navbar /><Home /></div>
   },
   {
    path: '/login',
    element :<div><Navbar /><Login /></div>
   },
   {
    path: '/signup',
    element :<div><Navbar /><SignUp /></div>
   },
   {
    path: '/about',
    element:<div><Navbar /><About /></div>
   },
   {
    
    path:'/loginsuccess',
    element:<div><UserNavbar userinfo={info} /><SuccessLogin userinfoafterlogin= {info} /></div>
   },
   {
    path:'/profile',
    element:<div><UserNavbar userinfo={info}/><Profile /></div>
   }
  ])
  return (
    <div>
    <RouterProvider router={router}></RouterProvider>
    </div>

  );
}

export default App;
