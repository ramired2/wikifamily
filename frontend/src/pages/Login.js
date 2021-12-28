import React, {useState, useEffect} from 'react'
// for backend -- {useState, useEffect}

const Login = ({
}) => {
  return(
    <div className="content">
        <a href="http://localhost:3000/auth/google">
            <p>Google</p>
        </a>

        <a href="http://localhost:3000/auth/facebook/wikifam/facebook">FB</a>
    </div>
  );
}

export default Login;