import os
import argparse
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
import csv
import re
import pandas as pd


def update_metadata(doc: Document):
    # Lấy nội dung văn bản
    text = doc.page_content

    metadata = {}

    metadata['link'] = re.search(r'link:\s*(https?://\S+)', text)
    metadata['link'] = metadata['link'].group(1) if metadata['link'] else "N/A"

    metadata['loai_van_ban'] = re.search(r'loai_van_ban:\s*(\S.+)', text)
    metadata['loai_van_ban'] = metadata['loai_van_ban'].group(1) if metadata['loai_van_ban'] else "N/A"

    metadata['ngay_ban_hanh'] = re.search(r'ngay_ban_hanh:\s*(\S.+)', text)
    metadata['ngay_ban_hanh'] = metadata['ngay_ban_hanh'].group(1) if metadata['ngay_ban_hanh'] else "N/A"

    metadata['noi_ban_hanh'] = re.search(r'noi_ban_hanh:\s*(\S.+)', text)
    metadata['noi_ban_hanh'] = metadata['noi_ban_hanh'].group(1) if metadata['noi_ban_hanh'] else "N/A"

    metadata['so_hieu'] = re.search(r'so_hieu:\s*(\S+)', text)
    metadata['so_hieu'] = metadata['so_hieu'].group(1) if metadata['so_hieu'] else "N/A"

    metadata['title'] = re.search(r'title:\s*(\S.+)', text)
    metadata['title'] = metadata['title'].group(1) if metadata['title'] else "N/A"

    metadata['van_ban_duoc_dan'] = re.search(r'van_ban_duoc_dan:\s*(\{.+\})', text)
    metadata['van_ban_duoc_dan'] = metadata['van_ban_duoc_dan'].group(1) if metadata['van_ban_duoc_dan'] else "N/A"

    # Cập nhật metadata vào document
    doc.metadata.update(metadata)

    return doc


def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    csv.field_size_limit(10**6)
    loader = CSVLoader(file_path, encoding="utf-8")
    
    try:
        documents = loader.load()
    except Exception as e:
        raise ValueError(f"Failed to load CSV file '{file_path}': {e}")
    
    updated_documents = [update_metadata(doc) for doc in tqdm(documents)]
    
    return updated_documents


def create_chroma_db(documents, persist_dir, batch_size=1000):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    print(f"Number of chunks: {len(docs)}")
    
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir)
    
    vector_db = None
    for i in tqdm(range(0, len(docs), batch_size)):
        batch = docs[i:i+batch_size]
        
        if vector_db is None:
            vector_db = Chroma.from_documents(documents=batch, embedding=embeddings, persist_directory=persist_dir)
        else:
            vector_db.add_documents(batch)
        
        print(f"Persisted batch {i//batch_size + 1}")

    print(f"Database persisted to {persist_dir}")
    
    return vector_db


def load_chroma_db(persist_dir):
    if not os.path.exists(persist_dir):
        raise FileNotFoundError(f"The directory '{persist_dir}' does not exist.")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Load the Chroma vector store
    vector_db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vector_db


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Process CSV file and manage Chroma vector database.")
    parser.add_argument("file_path", type=str, help="Path to the CSV file containing data.")
    parser.add_argument("persist_directory", type=str, help="Directory to save or load the Chroma vector database.")
    args = parser.parse_args()

    try:
        # Load data from CSV file
        documents = load_data(args.file_path)
        
        # Create Chroma vector database and persist it
        chroma_db = create_chroma_db(documents, args.persist_directory)
        
        # Load the existing Chroma vector database
        loaded_db = load_chroma_db(args.persist_directory)
        
        # Check how many documents are in the loaded Chroma database
        print(f"Loading successful !!!")
    
    except Exception as e:
        print(f"Error: {e}")
