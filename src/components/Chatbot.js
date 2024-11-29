import React, { useState } from "react";
import "../styles/Chatbot.css";
import chatbotImage from "../assets/images/chatbot.png";

const Chatbot = () => {
  const [inputValue, setInputValue] = useState(""); // State lưu giá trị của message-input

  // Hàm xử lý khi nhấn button
  const handleQuestionClick = (question) => {
    setInputValue(question); // Cập nhật giá trị của inputValue
  };

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
        <button
          className="question-button"
          onClick={() => handleQuestionClick("Luật sở hữu trí tuệ là gì ?")}
        >
          Luật sở hữu trí tuệ là gì ?
        </button>
        <button
          className="question-button"
          onClick={() =>
            handleQuestionClick(
              "Hợp đồng chuyển giao công nghệ trong nước có được sử dụng ngôn ngữ tiếng Anh không?"
            )
          }
        >
          Hợp đồng chuyển giao công nghệ trong nước có được sử dụng ngôn ngữ
          tiếng Anh không?
        </button>
        <button
          className="question-button"
          onClick={() =>
            handleQuestionClick(
              "Bài giảng có được xem là một tài sản trí tuệ không ?"
            )
          }
        >
          Bài giảng có được xem là một tài sản trí tuệ không ?
        </button>
        <button
          className="question-button"
          onClick={() =>
            handleQuestionClick(
              "Các lần đổi mới gần đây của luật sở hữu trí tuệ ?"
            )
          }
        >
          Các lần đổi mới gần đây của luật sở hữu trí tuệ ?
        </button>
        <button
          className="question-button"
          onClick={() =>
            handleQuestionClick(
              "Mức phạt cao nhất khi vi phạm quyền tác giả là bao nhiêu ?"
            )
          }
        >
          Mức phạt cao nhất khi vi phạm quyền tác giả là bao nhiêu ?
        </button>
        <button
          className="question-button"
          onClick={() =>
            handleQuestionClick(
              "Sinh viên dùng sách, tài liệu, giáo trình photo bản sao có bị coi là vi phạm luật sở hữu trí tuệ không ?"
            )
          }
        >
          Sinh viên dùng sách, tài liệu, giáo trình photo bản sao có bị coi là
          vi phạm luật sở hữu trí tuệ không ?
        </button>
      </div>
      <div className="chatbot-message">
        <input
          type="text"
          placeholder="Message with iLaw"
          className="message-input"
          value={inputValue} // Kết nối state inputValue với value của input
          onChange={(e) => setInputValue(e.target.value)} // Cập nhật giá trị state khi nhập thủ công
        />
        <button className="send-button">↑</button>
      </div>
    </div>
  );
};

export default Chatbot;
