# Back end Ứng dụng iLaw

## Cài đặt

- Cài đặt environment:
```bash
pip install -r environments.txt
```
- Thêm file `.env` vào thư mục backend với nội dung:
``` bash
OPENAI_API_KEY=your_openai_api_key
```

- Tạo vectordatabase: 
```bash
python .\handlers\chroma_loader.py .\data\So-huu-tri-tue-processed.csv vector_db

```

- Khỏi chạy server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Kết nối FastAPI 

Kết nối tới `localhost:8000/chatbot/ask` với phương thức POST và headers
```json
{
    "Content-Type": "application/json"
}
```
và body
```json
{
    "question": "Câu hỏi của bạn"
}
```

Kết quả trà về là một json với cấu trúc
```json
{
    "question": "Câu hỏi của bạn",
    "answer": "Câu trả lời của chatbot",
    "links": [ "link1", "link2", "link3", "link4"],
    "titles": [ "title1", "title2", "title3", "title4"]
}
```


