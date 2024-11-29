import React from "react";
import "../styles/Chatbot.css";
import chatbotImage from "../assets/images/chatbot.png";

const Chatbot = () => {
  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <img
          src={chatbotImage} // Thay bằng đường dẫn logo của bạn
          alt="iLAW Logo"
          className="chatbot-logo"
        />
        <h1 className="chatbot-title">
          Xin chào, tôi có thể giúp gì được cho bạn ?
        </h1>
      </div>
      <div className="chatbot-questions">
        <button className="question-button">Luật sở hữu trí tuệ là gì ?</button>
        <button className="question-button">
          Hợp đồng chuyển giao công nghệ trong nước có được sử dụng ngôn ngữ
          tiếng Anh không?
        </button>
        <button className="question-button">
          Bài giảng có được xem là một tài sản trí tuệ không ?
        </button>
        <button className="question-button">
          Các lần đổi mới gần đây của luật sở hữu trí tuệ ?
        </button>
        <button className="question-button">
          Mức phạt cao nhất khi vi phạm quyền tác giả là bao nhiêu ?
        </button>
        <button className="question-button">
          Sinh viên dùng sách, tài liệu, giáo trình photo bản sao có bị coi là
          vi phạm luật sở hữu trí tuệ không ?
        </button>
      </div>
      <div className="chatbot-message">
        <input
          type="text"
          placeholder="Message with iLaw"
          className="message-input"
        />
        <button className="send-button">↑</button>
      </div>
    </div>
  );
};

export default Chatbot;
