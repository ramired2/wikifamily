import React, {useState, useEffect} from 'react';

/* we may need to make nav bar responsive:
 * depending on the screen size, the nav bar options and login btns turns into
 * hamburger menu (without logo though) */

// function ForNav() {
//   const [data, setData] = useState([]);

//   useEffect(() => { fetch('http://localhost:3000/name').then(res => res.json()).then(data => setData(data)).catch(console.error); }, []);

//   console.log(data);

// }

const Navbar = ({
  }) => {
    return(
      <div className="nav">
          <div className="navLogo">
            <img className="logo"  src="/logo192_70x70.png" alt="wikiFamily Logo" />
          </div>
          <div className="navLinks">
            <ul className="nav_list">
              <li id="nav_item" className="active"><a href="/">Home</a></li>
              <li id="nav_item"><a href="/create">CreateTree</a></li>
              <li id="nav_item"><a href="/help">Help</a></li>
              <li id="nav_item"><a href="/about">About</a></li>
            </ul>
          </div>
          <div className="accountContainer">
            <button type="button" className="accountBtns leftButton"><a href="/login">Login</a></button>
            <button type="button" className="accountBtns rightButton"><a href="http://localhost:3000/logout">Logout</a></button>
          </div>
      </div>
    );
  }
  export default Navbar;
