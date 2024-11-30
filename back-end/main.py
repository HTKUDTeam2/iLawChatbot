from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chatbot import router as chatbot_router
from handlers.chroma_loader import load_chroma_db

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Chatbot RAG API",
    version="1.0.0",
    description="An API for Chatbot using RAG pipeline."
)
# Cấu hình CORS cho phép gọi API từ bất kỳ domain nào
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Tải vector database khi ứng dụng khởi động
@app.on_event("startup")
async def load_existing_chroma_db():
    """
    Hàm được gọi khi ứng dụng khởi động.
    Tải vector database từ thư mục đã lưu và in ra một số nội dung mẫu.
    """
    try:
        print("Loading Chroma database...")
        app.state.chroma_db = load_chroma_db("vector_db")
        if (app.state.chroma_db is None):
            raise Exception("Failed to load Chroma database.")
        else:
            print("Chroma database loaded successfully.")

    except Exception as e:
        print(f"Failed to load Chroma database: {str(e)}")


# Gắn router cho chatbot
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])

# Xử lý lỗi khi ứng dụng dừng


@app.on_event("shutdown")
async def shutdown_event():
    """
    Hàm được gọi khi ứng dụng dừng.
    Có thể dùng để giải phóng tài nguyên nếu cần.
    """
    print("Shutting down application. Cleaning up resources.")

# Endpoint kiểm tra trạng thái ứng dụng


@app.get("/")
async def health_check():
    """
    Endpoint để kiểm tra trạng thái ứng dụng.
    """
    return {"status": "OK", "message": "Chatbot RAG API is running!"}
