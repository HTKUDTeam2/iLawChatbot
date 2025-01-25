import React, { useState, useRef, useEffect } from "react";
import "../styles/Chatbot.css";
import chatbotImage from "../assets/images/chatbot.png";
import userIcon from "../assets/images/user-icon.png";
import botIcon from "../assets/images/bot-icon.png";
import ReactMarkdown from "react-markdown";

const Chatbot = () => {
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]);
  const [showQuestions, setShowQuestions] = useState(true);
  const [showHeader, setShowHeader] = useState(true);
  const [response, setResponse] = useState(null);
  const inputRef = useRef(null);
  const [isTyping, setIsTyping] = useState(false);
  const [displayText, setDisplayText] = useState("");
  const chatDisplayRef = useRef(null);
  const [conversation, setConversation] = useState([]);

  const handleQuestionClick = (question) => {
    setInputValue(question);
    setTimeout(() => {
      if (inputRef.current) {
        inputRef.current.setSelectionRange(question.length, question.length);
        inputRef.current.focus();
      }
    }, 0);
  };

  const typeMessage = async (text, delay = 100) => {
    setIsTyping(true);
    const words = text.split(" ");
    let currentText = "";
    let wordIndex = 0;

    while (wordIndex < words.length) {
      // Random number of words (1-3) to show each time
      const wordsToShow = Math.floor(Math.random() * 3) + 1;
      const chunk = words.slice(wordIndex, wordIndex + wordsToShow).join(" ");

      currentText += (wordIndex > 0 ? " " : "") + chunk;
      setDisplayText(currentText);
      await new Promise((resolve) => setTimeout(resolve, delay));

      wordIndex += wordsToShow;
    }

    setIsTyping(false);
  };

  useEffect(() => {
    if (chatDisplayRef.current) {
      chatDisplayRef.current.scrollTop = chatDisplayRef.current.scrollHeight;
    }
  }, [messages, displayText]);

  const handleSendMessage = async () => {
    if (inputValue.trim()) {
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
            conversation, // Ngũ cảnh cuộc hội thoại
            currentQuestion: inputValue.trim(),
          }),
        });

        if (apiResponse.ok) {
          const data = await apiResponse.json();
          const updatedMessages = newMessages.slice(0, -1);
          const newBotMessage = {
            sender: "bot",
            text: data.answer,
            titles: data.titles,
            links: data.links,
          };
          
          const updatedConversation = [
            ...conversation, { question: inputValue.trim(), answer: data.answer },].slice(-5); 
          setConversation(updatedConversation);
          setMessages([...updatedMessages, newBotMessage]);
          await typeMessage(data.answer);
          setResponse(data);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
  };

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

      {!showQuestions && (
        <div className="chat-display" ref={chatDisplayRef}>
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
              <span className="chat-text">
                {msg.sender === "bot" &&
                msg.text === "Vui lòng đợi 1 chút nhé " ? (
                  <div className="loader"></div>
                ) : (
                  <>
                    <ReactMarkdown>
                      {msg.sender === "bot" && index === messages.length - 1
                        ? displayText
                        : msg.text}
                    </ReactMarkdown>
                    {msg.sender === "bot" &&
                      msg.titles &&
                      (!isTyping || index !== messages.length - 1) && (
                        <div className="references-section">
                          <p>
                            <strong>Trích dẫn nguồn:</strong>
                          </p>
                          <ul>
                            {msg.titles.map((title, idx) => (
                              <li key={idx}>
                                <a
                                  href={msg.links[idx]}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                >
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
      )}

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
