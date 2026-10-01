import os
import sys

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 현재 split_basic.py 위치
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# src/06 폴더의 절대경로
INGEST_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "06")
)

# Python 모듈 검색 경로에 src/06 추가
sys.path.insert(0, INGEST_DIR)

# src/06/ingestion.py에서 함수 가져오기
from injestion import load_documents


# manual.pdf 경로
DATA_PATH = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..", "data", "manual.pdf")
)

docs = load_documents(DATA_PATH)


splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 50,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function = len,
)

full_text = ""

for doc in docs:
    full_text += doc.page_content + "\n\n"

merged_doc = Document(page_content = full_text)

chunks = splitter.split_documents([merged_doc])

def show_boundary(chunks, index = 0):
    print(chunks[index].page_content[-80:])
    print()
    print(chunks[index+1].page_content[:80])
    print("-----0번 조각-----")
    print(chunks[0].page_content)
    print("-----------------")
    print("메타데이터:", chunks[0].metadata)
    print(docs[0].metadata)

show_boundary(chunks, 0)
