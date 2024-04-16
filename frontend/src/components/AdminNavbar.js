const AdminNavbar = () => {
    return (
      <nav className="navbar" >
        <h1>Welcome Administrator </h1>
        <div className="links">
          <a href="/admin">Home</a>
          <a href="/allusers">All Users</a>
          <a href="/allbookings">Bookings</a>
          <a href="/about" style={{ 
            color: 'white', 
            backgroundColor: '#f1356d',
            borderRadius: '8px' 
          }}>Log Out</a>
        </div>
      </nav>
    );
  }
   
  export default AdminNavbar;