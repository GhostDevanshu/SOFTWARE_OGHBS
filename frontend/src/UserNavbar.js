const UserNavbar = ({userinfo}) => {
    return (
      <nav className="navbar">
        <h1>Welcome {userinfo.first_name} {userinfo.last_name} </h1>
        <div className="links">

          <a href="/loginsuccess">Home</a>
          <a href="/loginsuccess/profile">Profile</a>
          <a href="/bookins">Book</a>
          
          <a href="/" style={{ 
            color: 'white', 
            backgroundColor: '#f1356d',
            borderRadius: '8px' 
          }}>LOG OUT</a>
        </div>
      </nav>
    );
  }

  export default UserNavbar;