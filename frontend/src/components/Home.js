import React from 'react';
import './Home.css';
import { ToastContainer,toast } from 'react-toastify';
const Home = () => {
  
  return (
    <div>
    <div className="home-container">
      <h1 className="welcome-text">Welcome to IIT KGP Guest House </h1>
    </div>
    <div class="guestHouses">
    <div class="guestHouse">
        <img class="guestHouseImg" src="/vgh.jpg" alt="Guest House"/>
        <div class="textBox" >
            <div class="guestHouseName">Technology Guest House</div>
        </div>
    </div>
    <div class="guestHouse">
        <div class="textBox">
            <div class="guestHouseName">Visveswaraya Guest House</div>
        </div>
        <img class="guestHouseImg" src="/tghfront.jpg" alt="Visveswaraya Guest House"/>
    </div>
    <div class="guestHouse">
        <img class="guestHouseImg" src="/tghfront.jpg" alt="Kolkata Guest House"/>
        <div class="textBox">
            <div class="guestHouseName">Kolkata Guest House</div>
        </div>
    </div>
</div>
<footer id="dk-footer" class="dk-footer">
            <div class="footerContainer" >
                <a name="footerid"></a>
                <div class="logo">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRORteuqtaG0f0C2WogImr0JL4ui6yAckU2-A&usqp=CAU" alt="footer_logo" class="img img-fluid"/>
                </div>
                <div class="info">
                        <div class="contact-us">
                            <div class="contact-icon">
                                <i class="fa fa-map-o" aria-hidden="true"></i>
                            </div>
                            <div class="contact-info">
                                <h3>Contact: </h3>
                                <p>Technology Guest House</p>
                                <p>IIT Kharagpur</p>
                                <p>Kharagpur, 721302</p>
                            </div>
                        </div>
                        <div class="contact-us">
                            <div class="contact-icon">
                                <i class="fa fa-volume-control-phone" aria-hidden="true"></i>
                            </div>
                            <div class="contact-info">
                                <h3>Phone Number: </h3>
                                <p>+91 7386120105</p>
                            </div>
                        </div>
                        <div class="contact-us email">
                            <div class="contact-icon">
                                <i class="fa fa-envelope" aria-hidden="true"></i>
                            </div>
                            <div class="contact-info">
                                <h3>Email</h3>
                                <p>oghbs@iitkgp.ac.in</p>
                            </div>
                        </div>
                </div>
            </div>
        <div class="copyright">
            <span>Copyright © 2024 All Right Reserved.</span>
            <div class="copyright-menu">
                <ul>
                    <li>
                        <a href="http://www.iitkgp.ac.in/">Home</a>
                    </li>
                    <li>
                        <a href="http://www.tgh.iitkgp.ac.in/?id=randc">Terms</a>
                    </li>
                    <li>
                        <a href="http://www.iitkgp.ac.in/">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
</footer>

    </div>
  );
};

export default Home;
