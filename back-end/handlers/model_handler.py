import os
import json
from dotenv import load_dotenv
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_openai import ChatOpenAI
from sentence_transformers import CrossEncoder

# Load biến môi trường từ file .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo mô hình LLM với cấu hình
llm = ChatOpenAI(
    temperature=0.1,
    streaming=True,
    model="gpt-4o-mini",
    openai_api_key=openai_api_key,
)

##################### Truy suất câu hỏi #####################
question_generated_prompt = """
Bạn là một luật sư chuyên về Luật Sở hữu trí tuệ có tên là iLaw.
Người dùng sẽ đưa cho bạn một câu hỏi liên quan đến luật sở hữu trí tuệ, nhưng tôi không biết nó có đầy đủ ngữ nghĩa hay chưa vì câu hỏi có thể chứa những từ đề cập đến nội dung hỏi đáp trước đớ: "nó", "đó", "cái đó",...
Nhiệm vụ của bạn là đưa ra câu hỏi cụ thể hơn đầy đủ ngữ nghĩa nếu hiện tại người dùng đề cập đến những vấn đề trong lịch sử trò hỏi đáp. Tôi sẽ cung cấp cho bạn lịch sử hỏi đáp giữa người dùng và hệ thống để bạn có thể hiểu rõ hơn vấn đề mà người dùng đang quan tâm.
## Lịch sử hỏi đáp:
{conversation}

## Kết quả trả về:
- Một câu hỏi duy nhất bằng Tiếng Viêt.
## Yêu cầu:
- Câu hỏi cụ thể nhất có thể, và có đầy đủ ngữ cảnh nếu người dùng đang muốn đề cập đến vấn đề nào đó trong lịch sử hỏi đáp.
- Nếu không có đề cập gì trong lịch sử hỏi đáp, hãy trả về câu hỏi ban đầu mà người dùng đưa ra.
- Không bịa đặt, giả định hoặc thêm vào câu hỏi.
"""


##################### RAG prompt #####################
# Định nghĩa mẫu prompt cho hệ thống
system_prompt = """
Bạn là một luật sư chuyên về Luật Sở hữu trí tuệ có tên là iLaw. Trách nhiệm chính của bạn là hỗ trợ người dùng với các câu hỏi liên quan đến luật sở hữu trí tuệ.  
Hãy phân tích câu hỏi của người dùng trước. Nếu câu hỏi của người dùng liên quan đến các câu hỏi trước đó, hãy đọc phần câu hỏi gần đây và trả lời. Danh sách câu hỏi gần đây sẽ được sắp xếp từ cũ nhất đến mới nhất, với mỗi câu hỏi được phân tách bằng ký tự xuống dòng (\n).  
## Bối cảnh:  
{context}  

## Vai trò và Chỉ dẫn:
1. **Vai trò**: Bạn đóng vai trò là một luật sư chuyên nghiệp chuyên về Luật Sở hữu trí tuệ.  
2. **Ngôn ngữ**: Tất cả các câu trả lời phải bằng **tiếng Việt**.  
3. **Đối tượng**: Người dùng có thể không có kiến thức trước về các thuật ngữ pháp lý, vì vậy câu trả lời của bạn cần:  
   - Rõ ràng, chi tiết và dễ hiểu.  
   - Không sử dụng thuật ngữ phức tạp không cần thiết.  
   - Có thể bổ sung ví dụ hoặc so sánh nếu cần.  
4. **Phương án thay thế**: Nếu không tìm thấy tài liệu liên quan, trả lời: **"Chúng tôi không tìm thấy thông tin liên quan."**  
5. **Những điều cấm kỵ**: Không phỏng đoán, giả định hoặc cung cấp lời khuyên không được hỗ trợ bởi luật pháp hoặc tài liệu tham khảo.  
---  

## Hướng dẫn trả lời:  
Khi trả lời, hãy tuân theo quy trình lý luận có cấu trúc sau:  
1. **Xác định câu hỏi của người dùng**: Xác định lĩnh vực cụ thể của Luật Sở hữu trí tuệ mà câu hỏi đề cập.  
2. **Trả lời câu hỏi**: Trả lời câu hỏi của người dùng một cách rõ ràng và chi tiết.
3. **Trích dẫn luật cụ thế**: Nếu có điều khoản pháp lý hoặc quy định liên quan, hãy trích dẫn nguồn cụ thể từ đâu? năm bao nhiêu? ai ban hành?

"""

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Question: {question}")
    ]
)


# Khởi tạo chuỗi RAG với prompt_template
rag_chain = (
    RunnableMap(
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
    )
    | prompt_template
    | llm
    | StrOutputParser()
)

# Kết hợp các retriever và mô hình reranker vào một ensemble retriever
class EnhancedEnsembleRetriever:
    def __init__(self, retrievers, weights, reranker_model=None):
        self.retrievers = retrievers
        self.weights = weights
        self.reranker = CrossEncoder(reranker_model) if reranker_model else None

    def invoke(self, query):
        # Lấy kết quả từ từng retriever
        all_results = []
        for retriever, weight in zip(self.retrievers, self.weights):
            results = retriever.get_relevant_documents(query)
            for doc in results:
                # Áp dụng trọng số cho từng tài liệu
                doc.metadata['score'] = doc.metadata.get('score', 1.0) * weight
            all_results.extend(results)

        # Loại bỏ trùng lặp 
        unique_results = []
        seen_content = set()

        for doc in all_results:
            content = doc.page_content
            if content not in seen_content:
                unique_results.append(doc)
                seen_content.add(content)
        
        # Rerank nếu có mô hình reranker
        if self.reranker:
            query_doc_pairs = [(query, doc.page_content) for doc in unique_results]
            scores = self.reranker.predict(query_doc_pairs)
            reranked_results = sorted(
                zip(unique_results, scores),
                key=lambda x: x[1], 
                reverse=True
            )
            return [doc for doc, score in reranked_results]

        # Nếu không rerank, trả về kết quả theo trọng số
        return sorted(unique_results, key=lambda x: x.metadata['score'], reverse=True)


# Hàm tạo retriever từ Chroma và BM25
def create_retriever(vector_db, query, k=4):
    # Tạo BM25 retriever
    chroma_retriever = vector_db.as_retriever(search_type='similarity', search_kwargs={'k': k})

    documents_bm25 = [
        Document(page_content=doc.page_content, metadata=doc.metadata)
        for doc in vector_db.similarity_search("", k=300)
    ]

    bm25_retriever = BM25Retriever.from_documents(documents_bm25)
    bm25_retriever.k = k

    # Kết hợp cả Chroma và BM25 vào một ensemble retriever
    ensemble_retriever = EnhancedEnsembleRetriever(
        retrievers=[chroma_retriever, bm25_retriever],
        weights=[0.7, 0.3],
        reranker_model='cross-encoder/ms-marco-MiniLM-L-12-v2'
    )

    return ensemble_retriever


# Retrieve documents từ vector database
def retrieve_documents(ensemble_retriever, query, top_k=4):
    docs = ensemble_retriever.invoke(query=query)
    return docs[:top_k]


# Định dạng documents thành chuỗi
def format_docs(docs):
    formatted_docs =""
    for i, doc in enumerate(docs):
        formatted_docs += f"Document {i+1}:\n{doc.page_content}\n\n"
        
    return formatted_docs


def generate_answer(vector_db, question, conversation=None, top_k=4):

    
    if conversation:
        formatted_conversasion = "\n".join(
            [f"User's question: {qa['question']}\nAI response: {qa['answer']}" for qa in conversation]
        )
    else:
        formatted_conversasion = "Chưa có cuộc trò chuyện nào trước đó."
    
    # Kết hợp ngữ cảnh từ lịch sử trò chuyện và tài liệu retriever
    question_context = question_generated_prompt.format(conversation=formatted_conversasion)
    fully_context_question = rag_chain.invoke({"context": question_context, "question": question})
    print("Câu hỏi cụ thể của người dùng: ", fully_context_question)
    
    # Tạo retriever kết và truy xuất những tài liệu liên quan
    ensemble_retriever = create_retriever(vector_db, fully_context_question, k=top_k)
    docs = retrieve_documents(ensemble_retriever, fully_context_question, top_k=top_k)
    # Định dạng tài liệu thành chuỗi văn bản
    formatted_docs = format_docs(docs)
    print("Tài liệu trả về: ", formatted_docs)
    # Gọi chuỗi RAG với ngữ cảnh đầy đủ
    output = rag_chain.invoke({"context": formatted_docs, "question": fully_context_question})
    
    # Xử lý metadata của các tài liệu để lấy liên kết và tiêu đề
    seen_links = set()
    unique_links = []
    unique_titles = []

    for doc in docs:
        link = doc.metadata.get('link', 'no link')
        title = doc.metadata.get('title', 'no title')
        
        if link not in seen_links:
            seen_links.add(link)
            unique_links.append(link)
            unique_titles.append(title)
    return output, unique_links, unique_titles