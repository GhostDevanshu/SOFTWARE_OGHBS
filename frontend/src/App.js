// App.js
import React from 'react';
import './App.css';
import Home from './components/Home';
import Login from './components/Login';
import SignUp from './components/SignUp';
import Navbar from './components/Navbar';
import {  createBrowserRouter,RouterProvider } from "react-router-dom";
import About from './components/About';
import Profile from './components/Profile';
import UserNavbar from './components/UserNavbar';
import ForUser from './components/ForUser';
import CheckAvailability from './components/CheckAvailability';
import Booking from './components/Booking';
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
    path:'/profile',
    element:<div><UserNavbar/><Profile /></div>
   },
   {
    path:'/home',
    element:<div><UserNavbar/><ForUser/></div>
   },
   {
    path:'/checkavailable',
    element:<div><UserNavbar/><CheckAvailability/></div>
   },
   {
    path:'/book',
    element:<div><UserNavbar/><Booking/></div>
   }
  ])
  return (
    <div>
      
    <RouterProvider router={router}></RouterProvider>
    </div>

  );
}

export default App;
