// App.js
import React from 'react';
import './App.css';
import Home from './Home';
import Login from './Login';
import SignUp from './SignUp';
import Navbar from './Navbar';
import SuccessLogin from './components/SuccessLogin';
import {  createBrowserRouter,RouterProvider } from "react-router-dom";
import About from './About';

function App() {
  const router =createBrowserRouter([
   {
    path: '/',
    element :<Home></Home>
   },
   {
    path: '/login',
    element :<Login></Login>
   },
   {
    path: '/signup',
    element :<SignUp></SignUp>
   },
   {
    path: '/about',
    element:<About></About>
   },
   {
    path:'/succeslogin',
    element:<SuccessLogin></SuccessLogin>
   }
  ])
  return (
    <div>
    <Navbar></Navbar>
    <RouterProvider router={router}></RouterProvider>
    </div>
  );
}

export default App;
