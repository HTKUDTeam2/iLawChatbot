import React, { useState } from "react";
import "../styles/CommonQA.css"; // Import file CSS

// Dữ liệu FAQ
const faqData = [
  {
    question:
      "Hồ sơ đăng ký chuyển giao công nghệ bao gồm những giấy tờ gì? Thời hạn cấp Giấy chứng nhận đăng ký chuyển giao công nghệ là bao lâu?",
    answer: `
      Hồ sơ đăng ký chuyển giao công nghệ bao gồm các giấy tờ sau:
      <ul>
        <li><strong>Đơn đăng ký chuyển giao công nghệ</strong>: Được kê khai theo mẫu quy định của cơ quan có thẩm quyền.</li>
        <li><strong>Bản sao Giấy chứng nhận đăng ký doanh nghiệp</strong> của tổ chức/cá nhân thực hiện chuyển giao công nghệ.</li>
        <li><strong>Bản sao hợp đồng chuyển giao công nghệ</strong> hoặc thỏa thuận giữa các bên, có thể bao gồm các điều khoản chi tiết về chuyển nhượng công nghệ, quyền sở hữu, và nghĩa vụ của các bên.</li>
        <li><strong>Bản mô tả công nghệ</strong> chuyển giao: Bao gồm các thông tin về công nghệ, quá trình chuyển giao, và ứng dụng công nghệ.</li>
        <li><strong>Bản sao các tài liệu liên quan</strong>: Giấy tờ chứng minh quyền sở hữu hoặc quyền sử dụng công nghệ của bên chuyển giao, chứng minh tính hợp pháp của công nghệ đó (nếu có).</li>
        <li><strong>Chứng nhận sở hữu trí tuệ</strong> (nếu có): Ví dụ, bản quyền sáng chế, bằng sáng chế hoặc các tài liệu liên quan đến quyền sở hữu trí tuệ của công nghệ.</li>
      </ul>

      <strong>Thời gian cấp Giấy chứng nhận đăng ký chuyển giao công nghệ:</strong> Thời gian cấp Giấy chứng nhận thường dao động từ <strong>15 đến 30 ngày</strong> kể từ ngày cơ quan có thẩm quyền nhận đầy đủ hồ sơ hợp lệ. Tuy nhiên, trong một số trường hợp phức tạp, thời gian có thể lâu hơn. Cơ quan có thẩm quyền chính là Bộ Khoa học và Công nghệ hoặc các cơ quan được phân cấp.

    `,
  },
  {
    question:
      "Những trường hợp nào khi chuyển giao công nghệ phải tiến hành đăng ký với cơ quan nhà nước?",
    answer: `
      Căn cứ <a href="https://thuvienphapluat.vn/van-ban/Thuong-mai/Luat-chuyen-giao-cong-nghe-2017-322937.aspx?anchor=dieu_31" target="_blank" class="faq-link">
      Điều 31 Luật Chuyển giao công nghệ 2017</a> quy định đăng ký chuyển giao công nghệ. 
      Khi chuyển giao công nghệ thuộc một trong các trường hợp sau thì phải đăng ký với cơ quan quản lý nhà nước về khoa học và công nghệ:
      <ul>
        <li>Chuyển giao công nghệ từ nước ngoài vào Việt Nam</li>
        <li>Chuyển giao công nghệ từ Việt Nam ra nước ngoài</li>
        <li>Chuyển giao công nghệ trong nước có sử dụng vốn nhà nước hoặc ngân sách nhà nước, 
        trừ trường hợp đã được cấp Giấy chứng nhận đăng ký kết quả thực hiện nhiệm vụ khoa học và công nghệ.</li>
      </ul>
      <strong>Lưu ý:</strong> <span class="highlight-red">Trừ công nghệ hạn chế chuyển giao đã được cấp Giấy phép chuyển giao công nghệ.</span>
    `,
  },
  {
    question: "Quyền sở hữu trí tuệ bao gồm những quyền gì?",
    answer:
      "Quyền sở hữu trí tuệ bao gồm quyền tác giả, quyền sở hữu công nghiệp và quyền đối với giống cây trồng.",
  },
];

const CommonQA = () => {
  const [activeIndex, setActiveIndex] = useState(null);

  const toggleAnswer = (index) => {
    setActiveIndex(activeIndex === index ? null : index);
  };

  return (
    <div className="faq-container">
      <h1 className="faq-header">Frequently Asked Question</h1>
      <div>
        {faqData.map((faq, index) => (
          <div className="faq-item" key={index}>
            <button
              className="faq-question"
              onClick={() => toggleAnswer(index)}
            >
              {faq.question}
              <span>{activeIndex === index ? "−" : "+"}</span>
            </button>
            {activeIndex === index && (
              <div
                className="faq-answer"
                dangerouslySetInnerHTML={{ __html: faq.answer }}
              ></div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommonQA;
