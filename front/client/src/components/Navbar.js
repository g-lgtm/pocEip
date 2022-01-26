import React from 'react';
import { NavLink } from "react-router-dom";

const Navbar = () => {
    return (
        <nav>
            <div class="nav-container">
                <div class="logo">
                    <NavLink exact to="/">
                        <div class="logo">
                            <img src="./img/logo.png" alt="icon" />
                            <h3>Flylens</h3>
                        </div>
                    </NavLink>
                </div>
                <ul>
                    <li className="welcome">
                        <NavLink exact to="/Mon-espace">
                            <h5>Mon espace</h5>
                        </NavLink>
                    </li>

                </ul>
            </div>
        </nav>
    );
};

export default Navbar;