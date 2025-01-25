from fastapi import APIRouter, HTTPException, Request
from handlers.model_handler import generate_answer
from schemas.chatbot import ChatbotRequest, ChatbotResponse

# Khởi tạo router cho chatbot
router = APIRouter()


@router.post("/ask", response_model=ChatbotResponse)
async def ask_question(request: ChatbotRequest, app_request: Request):
    current_question = request.currentQuestion
    conversation = request.conversation

    try:
        # Truy cập vector database đã được load sẵn trong app.state
        chroma_db = app_request.app.state.chroma_db

        # Sinh câu trả lời từ câu hỏi và lấy ngữ cảnh từ lịch sử trò chuyện
        answer, links, titles = generate_answer(
            vector_db=chroma_db,
            question=current_question,
            conversation=conversation,
            top_k=5
        )

        # Trả về câu trả lời
        return ChatbotResponse(question=current_question, answer=answer, links=links, titles=titles)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")