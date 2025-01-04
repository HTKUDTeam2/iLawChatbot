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

# Định nghĩa mẫu prompt cho hệ thống
system_prompt = """
You are an Intellectual Property Lawyer named iLaw. Your primary responsibility is to assist users with legal questions related to intellectual property law.
Please analyze the user's question first. If the user's question is related to previous questions, read the recent question section and answer. The list of recent questions will be sorted from oldest to newest, with each question separated by a \n character.
### Context:
{context}


### Role and Guidelines:
1. **Role**: You are acting as a professional lawyer specializing in Intellectual Property Law.
2. **Language**: All responses must be in **Vietnamese**.
3. **Audience**: Users may not have prior knowledge of legal terms, so your responses should be:
   - Clear, detailed, and easy to understand.
   - Free of unnecessary jargon.
   - Supplemented with examples or analogies when necessary.
4. **Fallback**: If no relevant documentation is found, respond with: **"Chúng tôi không tìm thấy thông tin liên quan."**
5. **Prohibited**: Do not guess, assume, or provide advice that cannot be supported by laws or references.
---

### Instructions:
When answering, follow this structured reasoning process:
1. **Identify the user's question**: Determine the specific area of Intellectual Property Law being addressed.
2. **Explain the concept in detail**: Provide a step-by-step explanation of relevant legal terms or laws.
3. **Apply to user's scenario**: Illustrate how the laws or terms apply to the user's context.
4. **Provide actionable advice**: Suggest next steps, documents, or authorities the user should contact.
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

class EnhancedEnsembleRetriever:
    def __init__(self, retrievers, weights, reranker_model=None):
        """
        Initialize the ensemble retriever with multiple retrievers and optional reranker.
        """
        self.retrievers = retrievers
        self.weights = weights
        self.reranker = CrossEncoder(reranker_model) if reranker_model else None

    def invoke(self, query):
        """
        Invoke the retrievers to get relevant documents and re-rank if necessary.
        """
        # 1. Lấy kết quả từ từng retriever
        all_results = []
        for retriever, weight in zip(self.retrievers, self.weights):
            results = retriever.get_relevant_documents(query)
            for doc in results:
                # Áp dụng trọng số cho từng tài liệu
                doc.metadata['score'] = doc.metadata.get('score', 1.0) * weight
            all_results.extend(results)

        # 2. Loại bỏ trùng lặp (nếu cần) theo nội dung
        unique_results = []
        seen_content = set()

        for doc in all_results:
            content = doc.page_content
            if content not in seen_content:
                unique_results.append(doc)
                seen_content.add(content)
        
        # 3. Rerank nếu có mô hình reranker
        if self.reranker:
            query_doc_pairs = [(query, doc.page_content) for doc in unique_results]
            scores = self.reranker.predict(query_doc_pairs)
            reranked_results = sorted(
                zip(unique_results, scores),
                key=lambda x: x[1],  # Sắp xếp theo điểm số
                reverse=True
            )
            return [doc for doc, score in reranked_results]

        # 4. Nếu không rerank, trả về kết quả theo trọng số
        return sorted(unique_results, key=lambda x: x.metadata['score'], reverse=True)


# Hàm tạo retriever từ Chroma và BM25
def create_retriever(vector_db, query, k=4):
    """
    Tạo một retriever kết hợp giữa Chroma và BM25 cho một cơ sở dữ liệu vector.
    """
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


# Hàm lấy tài liệu phù hợp từ retriever
def retrieve_documents(ensemble_retriever, query, top_k=4):
    """
    Lấy các tài liệu phù hợp từ ensemble retriever.
    """
    docs = ensemble_retriever.invoke(query=query)
    return docs[:top_k]


# Hàm định dạng tài liệu thành chuỗi
def format_docs(docs):
    """
    Định dạng các tài liệu thành chuỗi văn bản cho hệ thống RAG.
    """
    formatted_docs =""
    for i, doc in enumerate(docs):
        formatted_docs += f"Document {i+1}:\n{doc.page_content}\n\n"
        
    return formatted_docs


def generate_answer(vector_db, question, recent_interactions=None, top_k=4):
    """
    Sinh câu trả lời cho câu hỏi dựa trên cơ sở dữ liệu vector và danh sách tương tác gần nhất.
    
    Args:
        vector_db: Cơ sở dữ liệu vector để tìm kiếm tài liệu liên quan.
        question: Câu hỏi hiện tại từ người dùng.
        recent_interactions: Danh sách các câu hỏi và câu trả lời gần nhất, dạng:
                             [{"question": "...", "answer": "..."}, ...].
        top_k: Số lượng tài liệu liên quan tối đa cần truy xuất.
    
    Returns:
        output: Câu trả lời từ hệ thống.
        unique_links: Danh sách các liên kết duy nhất từ metadata của tài liệu.
        unique_titles: Danh sách tiêu đề tương ứng với các liên kết.
    """
    # Tạo retriever kết hợp
    ensemble_retriever = create_retriever(vector_db, question, k=top_k)
    
    # Lấy các tài liệu phù hợp
    docs = retrieve_documents(ensemble_retriever, question, top_k=top_k)
    
    # Định dạng tài liệu thành chuỗi văn bản
    formatted_docs = format_docs(docs)
    
    # Định dạng recent_interactions
    if recent_interactions:
        formatted_recent_interactions = "\n".join(
            [f"Q: {interaction['question']}\nA: {interaction['answer']}" for interaction in recent_interactions]
        )
    else:
        formatted_recent_interactions = "Không có tương tác gần đây."
    
    # Kết hợp ngữ cảnh từ recent_interactions và tài liệu
    full_context = f"""
    ### Recent Interactions:
    {formatted_recent_interactions}
    
    ### Relevant Documents:
    {formatted_docs}
    """

    # Gọi chuỗi RAG với ngữ cảnh đầy đủ
    output = rag_chain.invoke({"context": full_context, "question": question})
    
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


