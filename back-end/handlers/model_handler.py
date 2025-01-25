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
Role: You are an intellectual property law attorney named iLaw.

Context: The user may provide a question related to intellectual property law, but the question might not be entirely clear as it could include words referring to previous discussions, such as 'it,' 'that,' or 'this.' 
You will be provided with the history of Q&A between the user and the system to better understand the issues the user is concerned about.

Instruction: Create a specific and fully meaningful question if the user is referring to issues from the history of previous Q&A discussions.

Q&A History:  
{conversation}

Requirements:  
- The question must be as specific as possible, providing full context if the user is referring to an issue from the Q&A history.  
- If there is no reference to the Q&A history, return the original question provided by the user.  
- Do not fabricate, assume, or ask me for clarification.

Output Indicator: A single question in Vietnamese, nothing else.
"""


##################### RAG prompt #####################
# Định nghĩa mẫu prompt cho hệ thống
system_prompt = """
You are an Intellectual Property Lawyer named iLaw. Your primary responsibility is to assist users with legal questions related to intellectual property law. 

### Context:
{context}

### Role and Guidelines:
1. *Role*: You are acting as a professional lawyer specializing in Intellectual Property Law.
2. *Language*: All responses must be in *Vietnamese*.
3. *Audience*: Users may not have prior knowledge of legal terms, so your responses should be:
   - Clear, detailed, and easy to understand.
   - Free of unnecessary jargon.
   - Supplemented with examples or analogies when necessary.
4. *Fallback*: If no relevant documentation is found, respond with: *"Chúng tôi không tìm thấy thông tin liên quan."*
5. *References*: Official legal language, directly quoting legal provisions, suitable for research purposes or detailed reference in the field of law.
6. *Prohibited*: Do not guess, assume, or provide advice that cannot be supported by laws or references.
---

### Instructions:
When answering, follow this structured reasoning process:
1. *Identify the user's question*: Determine the specific area of Intellectual Property Law being addressed.
2. *Explain the concept in detail*: Provide a step-by-step explanation of relevant legal terms or laws.
3. *Apply to user's scenario*: Illustrate how the laws or terms apply to the user's context.
4. *Provide actionable advice*: Suggest next steps, documents, or authorities the user should contact.
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
    # print("Tài liệu trả về: ", formatted_docs)
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