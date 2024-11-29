import React, { useState, useRef } from "react";
import "../styles/Chatbot.css";
import chatbotImage from "../assets/images/chatbot.png"; // Thêm hình ảnh chatbot
import userIcon from "../assets/images/user-icon.png"; // Thêm hình ảnh icon người dùng
import botIcon from "../assets/images/bot-icon.png"; // Thêm hình ảnh icon bot

const Chatbot = () => {
  const [inputValue, setInputValue] = useState(""); // State lưu giá trị của message-input
  const [messages, setMessages] = useState([]); // State lưu danh sách tin nhắn
  const [showQuestions, setShowQuestions] = useState(true); // State kiểm soát việc hiển thị câu hỏi gợi ý
  const [showHeader, setShowHeader] = useState(true); // State kiểm soát việc hiển thị logo và câu chào
  const inputRef = useRef(null); // Tham chiếu đến input để kiểm soát con trỏ
  const responseChunkRef = useRef(""); // Tham chiếu đến kết quả hiện tại lưu lại từ stream trả về từ backend

  // Hàm truy vấn lấy kết quả từ model và cập nhật lại trên giao diện
  // Vẫn chưa làm được hiển thị kết quả kiểu stream nên chỉ hiện ra khi có đủ chuỗi kết quả
  function fetchModelStream(prompt) {
    console.log(messages)
    const queryParams = new URLSearchParams();
    queryParams.append("prompt", prompt);

    console.log("Messages:", messages);
    fetch("http://127.0.0.1:8000/model?" + queryParams.toString()).then((response) => {
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      var result = "";
      const readChunk = () => {
        return reader.read().then(({ done, value }) => {
            if (done) {
                return;
            }

            // Decode and append the new chunk to state
            const chunk = decoder.decode(value);
            
            responseChunkRef.current += chunk;
            // Continue reading the next chunk
            return readChunk();
        });
      };

      return readChunk();
    }).catch((err)=> {
      
      alert('Có lỗi xảy ra, vui lòng thử lại sau');

    }).finally(() => { 
      setMessages([
        ...messages,
        { sender: "you", text: prompt },
        { sender: "bot", text: responseChunkRef.current }, // Phản hồi bot
      ]);
      responseChunkRef.current = "";
    });
  }

  // Hàm xử lý khi nhấn câu hỏi gợi ý
  const handleQuestionClick = (question) => {
    setInputValue(question); // Cập nhật input với câu hỏi gợi ý

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
        { sender: "bot", text: "Vui lòng đợi 1 chút nhé " }, // Phản hồi bot
      ]);
      fetchModelStream(inputValue); // Gửi tin nhắn đến model và cập nhật kết quả
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

  return (
    <div className="chatbot-container">
      {showHeader && (
        <div className="chatbot-header">
          <img src={chatbotImage} alt="iLAW Logo" className="chatbot-logo" />
          <h1 className="chatbot-title">
            Xin chào, tôi có thể giúp gì được cho bạn ?
          </h1>
        </div>
      )}

      <div className="chat-display">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-bubble ${
              msg.sender === "you" ? "chat-you" : "chat-bot"
            }`}
          >
            <img
              src={msg.sender === "you" ? userIcon : botIcon}
              alt={msg.sender}
              className="chat-icon"
            />
            <span
              className={`chat-text ${msg.sender === "bot" ? "waiting" : ""}`}
            >
              {msg.sender === "bot" &&
              msg.text === "Vui lòng đợi 1 chút nhé " ? (
                <div className="loader"></div> // Hiển thị loader khi bot đang chờ
              ) : (
                msg.text
              )}
            </span>
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

      <div className="chatbot-message">
        <input
          type="text"
          placeholder="Message with iLaw"
          className="message-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          ref={inputRef}
        />
        <button className="send-button" onClick={handleSendMessage}>
          ↑
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
