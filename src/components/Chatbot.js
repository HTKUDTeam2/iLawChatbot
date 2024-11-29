import React, { useState, useRef, useEffect } from "react";
import "../styles/Chatbot.css";
import chatbotImage from "../assets/images/chatbot.png";

const Chatbot = () => {
  const [inputValue, setInputValue] = useState(""); // State lưu giá trị của message-input
  const [messages, setMessages] = useState([]); // State lưu danh sách tin nhắn
  const [showQuestions, setShowQuestions] = useState(true); // State kiểm soát việc hiển thị câu hỏi gợi ý
  const [showHeader, setShowHeader] = useState(true); // State kiểm soát việc hiển thị logo và câu chào
  const inputRef = useRef(null); // Tham chiếu đến input để kiểm soát con trỏ

  // Hàm xử lý khi nhấn câu hỏi gợi ý
  const handleQuestionClick = (question) => {
    setInputValue(question); // Cập nhật input với câu hỏi gợi ý
    //TODO: Ẩn các thuộc tính thừa và chuyển ngay đến giao diên chatbot
    // Nếu đã có API backend
    /*setShowQuestions(false); // Ẩn câu hỏi gợi ý sau khi nhấn
    setShowHeader(false);*/ // Ẩn header sau khi nhấn

    // Di chuyển con trỏ đến cuối câu hỏi gợi ý
    setTimeout(() => {
      if (inputRef.current) {
        inputRef.current.setSelectionRange(question.length, question.length);
        inputRef.current.focus(); // Đảm bảo trường nhập liệu được focus
      }
    }, 0); // Đảm bảo setSelectionRange được thực hiện sau khi render lại
  };

  // Hàm gửi tin nhắn
  const handleSendMessage = () => {
    if (inputValue.trim()) {
      // Thêm tin nhắn của người dùng vào danh sách tin nhắn
      setMessages([
        ...messages,
        { sender: "you", text: inputValue },
        { sender: "bot", text: "Vui lòng đợi 1 chút nhé ......." }, // Phản hồi bot
      ]);
      setInputValue(""); // Reset input sau khi gửi
      setShowQuestions(false); // Ẩn các câu hỏi gợi ý khi gửi tin nhắn
      setShowHeader(false); // Ẩn logo và câu chào khi gửi tin nhắn
    }
  };

  // Hàm xử lý khi nhấn phím Enter
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && inputValue.trim()) {
      handleSendMessage();
    }
  };

  // Di chuyển con trỏ về cuối mỗi khi inputValue thay đổi
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.setSelectionRange(inputValue.length, inputValue.length);
      inputRef.current.focus(); // Đảm bảo trường nhập liệu được focus
    }
  }, [inputValue]);

  return (
    <div className="chatbot-container">
      {/* Ẩn phần header khi showHeader là false */}
      {showHeader && (
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
      )}

      {/* Khu vực hiển thị tin nhắn */}
      <div className="chat-display">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-bubble ${
              msg.sender === "you" ? "chat-you" : "chat-bot"
            }`}
          >
            <span className="chat-text">{msg.text}</span>
          </div>
        ))}
      </div>

      {/* Khu vực câu hỏi gợi ý, chỉ hiển thị nếu showQuestions là true */}
      {showQuestions && (
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
      )}

      {/* Khu vực nhập tin nhắn */}
      <div className="chatbot-message">
        <input
          type="text"
          placeholder="Message with iLaw"
          className="message-input"
          value={inputValue} // Kết nối state inputValue với value của input
          onChange={(e) => setInputValue(e.target.value)} // Cập nhật giá trị state khi nhập thủ công
          onKeyDown={handleKeyDown} // Thêm sự kiện onKeyDown để gửi khi nhấn Enter
          ref={inputRef} // Tham chiếu đến input để di chuyển con trỏ
        />
        <button className="send-button" onClick={handleSendMessage}>
          ↑
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
