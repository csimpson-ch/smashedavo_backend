import React, { useState, useEffect } from 'react';
import { redirect } from "react-router-dom";
import '../static/bootstrap.min.css';


function Login () {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const login_url = 'http://127.0.0.1:8000/backend/login/';

    const handleSubmit = async (event) => {
        event.preventDefault();
        // alert('Form submitted with username: ' + username + ' and password: ' + password);
        // setUsername(username);
        // setPassword(password);

        // make a post request with username and password to backend
        const res = await fetch(login_url, {
            method: "POST",
            mode: "cors",
            credentials: "same-origin",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "username": username,
                "password": password
            }),
        });
        
        const json = await res.json();
        if (json.status === "Authenticated") {
            sessionStorage.setItem('username', json.username);
            alert('User ' + json.username + ' has been authenticated.');
        }
        else {
            alert("The user could not be authenticated.");
        }
    };

    return (

        <div>
            <h1>Login</h1>
            <form class="form-signin" onSubmit={handleSubmit} method="POST">

                <label for="username" class="sr-only">Username</label>
                <input
                    class="form-control"
                    type="text"
                    id="username"
                    name="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    autofocus
                />

                <label for="password" class="sr-only">Password</label>
                <input 
                    class="form-control"
                    type="password"
                    id="password"
                    name="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <br />
                <input type="submit" value="Login" class="btn btn-lg btn-primary btn-block" />
            </form>
        </div>
    )

}

export default Login
