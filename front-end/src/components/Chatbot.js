import React, { useState, useRef } from "react";
import "../styles/Chatbot.css";
import chatbotImage from "../assets/images/chatbot.png";
import userIcon from "../assets/images/user-icon.png";
import botIcon from "../assets/images/bot-icon.png";
import ReactMarkdown from 'react-markdown';

const Chatbot = () => {
   // State lưu giá trị của message-input
  const [inputValue, setInputValue] = useState("");
  // State lưu danh sách tin nhắn
  const [messages, setMessages] = useState([]);
   // State kiểm soát việc hiển thị câu hỏi gợi ý
  const [showQuestions, setShowQuestions] = useState(true);
  const [showHeader, setShowHeader] = useState(true); 
   // State lưu kết quả từ API
  const [response, setResponse] = useState(null);
   // Tham chiếu đến input để kiểm soát con trỏ
  const inputRef = useRef(null);
  // const [recentQuestions, setRecentQuestions] = useState([]);
  const [recentInteractions, setRecentInteractions] = useState([]);



  // Hàm xử lý khi nhấn câu hỏi gợi ý
  const handleQuestionClick = (question) => {
    // Cập nhật input với câu hỏi gợi ý
    setInputValue(question); 

    // Di chuyển con trỏ đến cuối câu hỏi gợi ý
    setTimeout(() => {
      if (inputRef.current) {
        inputRef.current.setSelectionRange(question.length, question.length);
        inputRef.current.focus(); 
      }
    }, 0);
  };

  // Hàm gửi tin nhắn và gọi API
  const handleSendMessage = async () => {
    if (inputValue.trim()) {
      // Thêm tin nhắn "đang chờ" vào danh sách tin nhắn
      const newMessages = [
        ...messages,
        { sender: "you", text: inputValue },
        { sender: "bot", text: "Vui lòng đợi 1 chút nhé " },
      ];
      setMessages(newMessages);
      setInputValue("");
      setShowQuestions(false);
      setShowHeader(false);
      setResponse(null);
  
      try {
        const apiResponse = await fetch("http://localhost:8000/chatbot/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            recentInteractions, // Gửi danh sách tương tác gần nhất (câu hỏi + câu trả lời)
            currentQuestion: inputValue.trim(), // Gửi câu hỏi hiện tại
          }),
        });
  
        if (apiResponse.ok) {
          const data = await apiResponse.json();
  
          // Thay thế tin nhắn "đang chờ" bằng câu trả lời từ API
          const updatedMessages = newMessages.map((msg) =>
            msg.text === "Vui lòng đợi 1 chút nhé "
              ? {
                  sender: "bot",
                  text: data.answer,
                  titles: data.titles,
                  links: data.links,
                }
              : msg
          );
  
          // Thêm câu hỏi và câu trả lời vào danh sách recentInteractions
          const updatedRecentInteractions = [
            ...recentInteractions,
            { question: inputValue.trim(), answer: data.answer },
          ].slice(-5); // Giữ tối đa 5 tương tác gần nhất
  
          setMessages(updatedMessages);
          setRecentInteractions(updatedRecentInteractions); // Cập nhật tương tác gần nhất
          setResponse(data);
        } else {
          console.error("API call failed");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
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
            className={`chat-bubble ${msg.sender === "you" ? "chat-you" : "chat-bot"}`}
          >
            <img
              src={msg.sender === "you" ? userIcon : botIcon}
              alt={msg.sender}
              className="chat-icon"
            />
            <span
              className={`chat-text ${msg.sender === "bot" && msg.text === "Vui lòng đợi 1 chút nhé " ? "waiting" : ""}`}
            >
              {msg.sender === "bot" && msg.text === "Vui lòng đợi 1 chút nhé " ? (
                <div className="loader"></div>
              ) : (
                <>
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                  {/* If we have response data, render the detailed info */}
                  {msg.sender === "bot" && msg.titles && (
                    <div>
                      <br />
                      <br />
                      <p><strong>Trích dẫn nguồn:</strong></p>
                      <ul>
                        {msg.titles.map((title, index) => (
                          <li key={index}>
                            <a href={msg.links[index]} target="_blank" rel="noopener noreferrer">
                              {title}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </>
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