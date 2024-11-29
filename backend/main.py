from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hàm sẽ gắn câu trả lời của mô hình, thay bằng chuỗi kết quả hàm gọi mô hình thực sự
# Nếu muốn trả về dạng stream, thì dùng yield với từng đoạn câu trả lời, 
# còn không thì return chuỗi kết quả, hoặc yield 1 lần duy nhất
async def model_response_generator(prompt: str = None):
    yield "Câu hỏi:\n"
    await asyncio.sleep(0.3)
    yield prompt + "\n"
    await asyncio.sleep(0.3)
    yield "Câu trả lời:\n"
    await asyncio.sleep(0.3)
    yield "Đây là một câu trả lời ví dụ\n"

@app.get("/model")
async def llama_stream(prompt: str = None):
    # Biến prompt là 1 query parameter mà frontend sẽ thêm vào từ prompt người dùng
    # gọi mô hình truyền tham số prompt vào
    return StreamingResponse(model_response_generator(prompt), media_type="text/plain")
