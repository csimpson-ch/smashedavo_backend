import React from 'react';
import { redirect } from "react-router-dom";
import '../static/bootstrap.min.css';


const Header = () => {

  async function handleLogout () {

    let username = sessionStorage.getItem('username');
    const logout_url = 'http://127.0.0.1:8000/backend/logout/';
  
    // make a post request with username and password to backend
    const res = await fetch(logout_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "username": username
            }),
        });
        
        const json = await res.json();
        if (json.status === "Logged out") {
            alert('User ' + username + ' has been logged out.');
            sessionStorage.removeItem('username');
        }
        else {
            alert("The user could not be logged out.");
        }
  }

  function User ({username}) {
    if (username == null) {
      return (
        <li class="nav-item">
          <a class="nav-link link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" href="/login">Login</a>
        </li>
      )
    } else {
      return (
        <form class="form-logout" onSubmit={handleLogout}>
          <button class="btn btn-outline-primary" type="submit">Logout ({username})</button>
        </form>
      )
    }
  }

  return (
      <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <div class="container-fluid">
            <a class="navbar-brand" href="/">Smashed Avacados</a>
              <button class="navbar-toggler collapsed" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
                    
              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                  <li class="nav-item">
                    <a class="nav-link" href="/blog">Blog</a>
                  </li>



                  <User username={sessionStorage.getItem('username')}/>

                </ul>
              </div>
          </div>
        </nav>
      </div>
  );
}

export default Header;
