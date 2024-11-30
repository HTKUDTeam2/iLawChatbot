# import json
import os

from dotenv import load_dotenv
from langchain.retrievers import  EnsembleRetriever
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
    temperature=0,
    streaming=True,
    model="gpt-4o-mini",
    openai_api_key=openai_api_key,
)

# Định nghĩa mẫu prompt
system = """You are a Intellectual property Lawer . Your name is iLaw. You are here to help people with their legal questions.
Here is the context you should refer to:
{context}
Your response must be in Vietnamese. 
If there is no relevant documentation, reply no data.
"""
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "Question: {question}")]
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
        self.retrievers = retrievers
        self.weights = weights
        self.reranker = CrossEncoder(reranker_model) if reranker_model else None

    def invoke(self, query):
        # 1. Lấy kết quả từ từng retriever
        all_results = []
        for retriever, weight in zip(self.retrievers, self.weights):
            results = retriever.get_relevant_documents(query)
            for doc in results:
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

    # Tạo BM25 retriever
    chroma_retriever = vector_db.as_retriever(search_type='similarity', search_kwargs={'k': 4})

    documents_bm25 = [
        Document(page_content=doc.page_content, metadata=doc.metadata)
        for doc in vector_db.similarity_search("", k=300)
    ]

    bm25_retriever = BM25Retriever.from_documents(documents_bm25)
    bm25_retriever.k = 4

    ensemble_retriever = EnhancedEnsembleRetriever(
        retrievers=[chroma_retriever, bm25_retriever],
        weights=[0.7, 0.3],
        reranker_model='cross-encoder/ms-marco-MiniLM-L-12-v2'
    )

    return ensemble_retriever


# Hàm lấy tài liệu phù hợp từ retriever
def retrieve_documents(ensemble_retriever, query, top_k=4):
    docs = ensemble_retriever.invoke(query=query)
    return docs[:top_k]
# Hàm định dạng tài liệu thành chuỗi
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Hàm gọi chuỗi RAG và sinh câu trả lời
def generate_answer(vector_db, question, top_k=4):
    ensemble_retriever = create_retriever( vector_db, question, k=top_k)
    docs = retrieve_documents(ensemble_retriever, question, top_k=top_k)
    seen_links = set()
    unique_links = []
    unique_titles = []

    # Lấy những thông tin cần thiết từ metadata của tài liệu: link, title
    for doc in docs:
        link = doc.metadata['link']
        title = doc.metadata['title']
        
        if link not in seen_links:
            seen_links.add(link)
            unique_links.append(link)
            unique_titles.append(title)
        
    formatted_docs = format_docs(docs)
    output = rag_chain.invoke({"context": formatted_docs, "question": question})
    # output = remove_json_formatting(output)
    print(formatted_docs)
    return output, unique_links, unique_titles
