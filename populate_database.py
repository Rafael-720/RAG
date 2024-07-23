import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from get_embedding_function import get_embedding_function


#python populate_database.py --reset

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument("--add", type=str, help="Path to the PDF file to add.")
    parser.add_argument("--list", action="store_true", help="List all documents in the database.")
    args = parser.parse_args()

    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    if args.add:
        print(f"📄 Adding document: {args.add}")
        add_document(args.add)
    elif args.list:
        list_documents()
    else:
        documents = load_documents(DATA_PATH)
        chunks = split_documents(documents)
        add_to_chroma(chunks)

def add_document(file_path):
    documents = load_document(file_path)
    chunks = split_documents(documents)
    add_to_chroma(chunks)

def load_documents(directory):
    document_loader = PyPDFDirectoryLoader(directory)
    return document_loader.load()

def load_document(file_path):
    document_loader = PyPDFDirectoryLoader(file_path)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks

def list_documents():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    existing_items = db.get(include=["metadatas"])
    existing_ids = set(existing_items["ids"])
    print(f"Number of documents in DB: {len(existing_ids)}")
    for doc_id, metadata in zip(existing_items["ids"], existing_items["metadatas"]):
        print(f"ID: {doc_id}, Metadata: {metadata}")

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
