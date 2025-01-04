# Chatbot Luật sở hữu trí tuệ - iLawChatbot
Nhóm 2 - Học thống kê ngôn ngữ và ứng dụng 
Thành viên 

| Họ và tên                    | MSSV     | Github            |
| ---------------------------- | -------- | ----------------- |
| Nguyễn Văn Quang Hưng        | 21120247 | @HungLVT          |
| Huỳnh Trí Nhân               | 21120302 | @HuynhTriNhan     |
| Tống Nguyễn Minh Khang       | 21120263 | @jesse-tong       |
| Trần Thị Kim Huỳnh           | 21120607 | @TranThiKimHuynh  |


## 1. Giới thiệu

iLawChatbot là một chatbot được xây dựng dựa trên mô hình RAG (Retrieval-Augmented Generation) để trả lời các câu hỏi liên quan đến lĩnh vực luật sở hữu trí tuệ với nguồn tài liệu lấy từ trang chủ [Thư viện Pháp Luật](https://thuvienphapluat.vn/). Chatbot này sử dụng mô hình RAG để truy xuất thông tin từ tập dữ liệu văn bản và sinh câu trả lời dựa trên thông tin truy xuất được. Các bạn có thể tìm đọc những câu hỏi về lĩnh vực luật sở hữu trí tuệ và thử nghiệm chatbot này tại [đây](https://thuvienphapluat.vn/hoi-dap-phap-luat/so-huu-tri-tue)

## 2. Cài đặt

### 2.1. Cài đặt môi trường  back-end
Vào thư mục backend và thực hiện các bước sau: 
1. Cài đặt environment:
```bash
pip install -r environments.txt
```
2. Thêm file `.env` vào thư mục backend với nội dung:
``` bash
OPENAI_API_KEY=your_openai_api_key
```

3. Tạo vectordatabase: 
```bash
 python .\handlers\chroma_loader.py .\data\So-huu-tri-tue-processed.csv vector_db

```
4. Khỏi chạy server:
```bash
uvicorn main:app --host localhost --port 8000 --reload
```
### 2.2 Khởi chạy chương trình front-end React

Ở trong thư mục front-end thực hiện các bước sau: 
1. Cài đặt các module cần thiết:
```bash
npm install
```

2. Build chương trình:
```bash
npm run build
```

3. Khởi chạy chương trình:
```bash
npm start
```

- Chương trình sẽ chạy ở địa chỉ `localhost:3000`


