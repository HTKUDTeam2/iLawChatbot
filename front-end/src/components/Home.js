import React from "react";
import "../styles/Home.css";
import homeImage from "../assets/images/Logo_main.png";

const Home = () => {
  return (
    <div className="home">
      <div>
        <h1>
          Welcome to <span>iLaw</span> 👋
        </h1>
        <p className="slogan">"Smart Answers, Anytime, Anywhere!"</p>
      </div>
      <div className="home-image-container">
        <div className="home-intro">
          <p className="home-text-box">
            Meet <strong>iLaw</strong>, your smart chatbot for all things
            intellectual property! From copyright to patents,{" "}
            <strong>iLaw</strong> delivers quick, accurate answers to your IP
            questions—anytime, anywhere.
          </p>
        </div>
        <div className="home-image">
          <img src={homeImage} alt="iLaw graphic" />
        </div>
      </div>
    </div>
  );
};

export default Home;
