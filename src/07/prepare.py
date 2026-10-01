import os
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------------------------
# 1. 경로 설정
# --------------------------------------------------

# 현재 파일이 있는 폴더: D:\RAG_Project\src\07
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# ingestion.py가 있는 폴더: D:\RAG_Project\src\06
INGEST_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "06")
)

# Python이 src\06 폴더에서도 모듈을 찾도록 설정
sys.path.insert(0, INGEST_DIR)

# src\06\injestion.py에서 함수 가져오기
from injestion import load_documents


# --------------------------------------------------
# 2. Chunk 설정
# --------------------------------------------------

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


# --------------------------------------------------
# 3. 문서 분할 함수
# --------------------------------------------------

def prepare_chunks(path: str):

    # 문서 불러오기
    docs = load_documents(path)

    # 문서가 없는 경우
    if not docs:
        print("불러온 문서가 없습니다.")
        return []

    # Text Splitter 설정
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    # 문서를 Chunk로 분할
    chunks = splitter.split_documents(docs)

    # Chunk가 없는 경우
    if not chunks:
        print("생성된 Chunk가 없습니다.")
        return []

    # 각 Chunk에 번호 추가
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

        # page_no가 없는 경우 page 값을 이용
        if "page_no" not in chunk.metadata:
            page = chunk.metadata.get("page")

            if isinstance(page, int):
                chunk.metadata["page_no"] = page + 1
            else:
                chunk.metadata["page_no"] = "?"

    # 각 Chunk의 글자 수
    lengths = [
        len(chunk.page_content)
        for chunk in chunks
    ]

    # 결과 출력
    print("=" * 50)
    print(f"조각 {len(chunks)}개 생성")
    print(
        f"평균 {sum(lengths) // len(lengths)}자, "
        f"최소 {min(lengths)}자, "
        f"최대 {max(lengths)}자"
    )

    # 너무 짧은 Chunk 확인
    if min(lengths) < 50:
        print("50자 미만 조각이 있습니다. chunk_size 확인 권장")

    print("=" * 50)

    return chunks


# --------------------------------------------------
# 4. 실행
# --------------------------------------------------

if __name__ == "__main__":

    # manual.pdf 절대경로
    PDF_PATH = os.path.abspath(
        os.path.join(
            CURRENT_DIR,
            "..",
            "..",
            "data",
            "manual.pdf"
        )
    )

    chunks = prepare_chunks(PDF_PATH)

    # 처음 3개 Chunk 확인
    for chunk in chunks[:3]:

        print(
            f"\n"
            f"[{chunk.metadata['chunk_id']}번 chunk | "
            f"p.{chunk.metadata['page_no']}]"
        )

        print(chunk.page_content[:100])