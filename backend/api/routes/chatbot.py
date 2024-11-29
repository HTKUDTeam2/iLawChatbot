from fastapi import APIRouter, HTTPException, Request
from handlers.model_handler import generate_answer
from schemas.chatbot import ChatbotRequest, ChatbotResponse

# Khởi tạo router cho chatbot
router = APIRouter()


@router.post("/ask", response_model=ChatbotResponse)
async def ask_question(request: ChatbotRequest, app_request: Request):
    """
    Endpoint xử lý câu hỏi từ người dùng.
    - Truy xuất tài liệu từ vector database.
    - Sinh câu trả lời dựa trên tài liệu.
    """
    question = request.question

    try:
        # Truy cập vector database đã được load sẵn trong app.state
        chroma_db = app_request.app.state.chroma_db

        # Sinh câu trả lời từ các tài liệu truy xuất
        answer, links, titles = generate_answer(vector_db=chroma_db, question=question, top_k=5)

        # Trả về câu trả lời
        return ChatbotResponse(question=question, answer=answer, links=links, titles=titles)

    except Exception as e:
        # Xử lý lỗi chung
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
