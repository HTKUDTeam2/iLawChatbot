import React from "react";
import "../styles/About.css";
import homeImage from "../assets/images/Logo_main.png";

const About = () => {
  return (
    <div className="about">
      <div>
        <h1>🫂 About us</h1>
        <p className="slogan">We‘re a group of students in HCMUS</p>
      </div>
      <div className="about-image-container">
        <div className="about-intro">
          <p className="about-text-box">
            ---- <strong> Team 2 </strong> ---
            <br />
            21120247 _ Nguyễn Văn Quang Hưng <br />
            21120302 _ Huỳnh Trí Nhân <br />
            21120263 _ Tống Nguyễn Minh Khang <br />
            21120607 _ Trần Thị Kim Huỳnh
          </p>
        </div>

        <div className="about-image">
          <img src={homeImage} alt="iLaw graphic" />
        </div>
      </div>
    </div>
  );
};

export default About;
