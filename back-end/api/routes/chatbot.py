from fastapi import APIRouter, HTTPException, Request
from handlers.model_handler import generate_answer
from schemas.chatbot import ChatbotRequest, ChatbotResponse

# Khởi tạo router cho chatbot
router = APIRouter()


@router.post("/ask", response_model=ChatbotResponse)
async def ask_question(request: ChatbotRequest, app_request: Request):
    """
    Endpoint xử lý câu hỏi từ người dùng.
    """
    current_question = request.currentQuestion
    recent_interactions = request.recentInteractions

    try:
        # Truy cập vector database đã được load sẵn trong app.state
        chroma_db = app_request.app.state.chroma_db

        # Sinh câu trả lời từ tài liệu và danh sách tương tác gần nhất
        answer, links, titles = generate_answer(
            vector_db=chroma_db,
            question=current_question,
            recent_interactions=recent_interactions,  # Truyền tương tác gần nhất
            top_k=5
        )

        # Trả về câu trả lời
        return ChatbotResponse(question=current_question, answer=answer, links=links, titles=titles)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

