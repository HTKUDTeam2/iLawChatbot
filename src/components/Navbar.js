import React from "react";
import { NavLink } from "react-router-dom";
import "../styles/Navbar.css";
import ilawLogo from "../assets/images/Logo_Web.png";

const Navbar = () => {
  return (
    <div className="navigationContainer">
      <div className="navigationWrapper">
        {/* Navigation Links */}
        <div className="navigationLinksContainer">
          <ul className="navigationLinks">
            <li>
              <NavLink
                to="/"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                Home
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/common-qa"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                Common Q&A
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/chatbot"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                Chatbot
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/about"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                About us
              </NavLink>
            </li>
          </ul>
        </div>
        {/* Logo */}
        <div className="logoContainer">
          <img src={ilawLogo} alt="iLAW Logo" className="logo" />
        </div>
      </div>
    </div>
  );
};

export default Navbar;
