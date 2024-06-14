import React from 'react';
import { redirect } from "react-router-dom";
import '../static/bootstrap.min.css';


const Sidebar = () => {
  return (
    <div class="col-2 bd-sidebar">
        <ul class="nav flex-column">
            <li class="nav-item">
                <a class="nav-link active" href="#">Create</a>
            </li>
            <li class="nav-item">
                <a class="nav-link active" href="/expenses">Expenses</a>
            </li>
        </ul>
    </div>
  );
}

export default Sidebar;
