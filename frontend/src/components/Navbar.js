const Navbar = () => {
    return (
      <nav className="navbar">
        <h1>IIT KGP Guest House </h1>
        <div className="links">
          <a href="/">Home</a>
          <a href="/login">Login</a>
          <a href="/signup">Signup</a>
          <a href="/loginsuccess">loginsuccess</a>
          <a href="/about" style={{ 
            color: 'white', 
            backgroundColor: '#f1356d',
            borderRadius: '8px' 
          }}>About</a>
        </div>
      </nav>
    );
  }
   
  export default Navbar;