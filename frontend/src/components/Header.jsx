import React from 'react';
import '../static/bootstrap.min.css';

const Header = () => {
  return (
    <html lang="EN">
      <head>
        <meta charset="UTF-8">
        </meta>
      </head>
      <body>
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
                  <li class="nav-item">
                    <a class="nav-link" href="/mortgage/login">Login</a>
                  </li>

                </ul>
              </div>
          </div>
        </nav>
    
        <div class="container-fluid">
          <div class="row">
            <div class="col-2 bd-sidebar">
              <ul class="nav flex-column">
                <li class="nav-item">
                  <a class="nav-link active" href="#">Create</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}

export default Header;
