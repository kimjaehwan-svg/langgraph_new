from langchain_community.document_loaders import PyPDFLoader


def validate(docs):
    # 1. 문서가 비어 있는지 확인
    if not docs:
        print("문서가 로드되지 않았습니다.")
        return

    # 2. 전체 페이지 수 확인
    print(f"전체 페이지 수: {len(docs)}")

    # 3. 빈 페이지 또는 텍스트가 거의 없는 페이지 확인
    empty_pages = []

    for i, doc in enumerate(docs, start=1):
        text = doc.page_content.strip()

        if len(text) < 10:
            empty_pages.append(i)

    if empty_pages:
        print(f"내용이 거의 없는 페이지: {empty_pages}")
        print("스캔 PDF이거나 텍스트 추출이 제대로 되지 않았을 수 있습니다.")
    else:
        print("빈 페이지 없음")

    # 4. 전체 글자 수 확인
    total_len = sum(len(doc.page_content) for doc in docs)
    print(f"전체 글자 수: {total_len}")

    # 5. 페이지별 글자 수 확인
    for i, doc in enumerate(docs, start=1):
        print(f"{i}페이지 글자 수: {len(doc.page_content)}")

    # 6. 첫 페이지 내용 일부 확인
    print("-" * 50)
    print("첫 페이지 내용 일부:")
    print(docs[0].page_content[:300])
    print("-" * 50)

    # 7. 메타데이터 확인
    print("첫 페이지 metadata:")
    print(docs[0].metadata)


# PDF 파일 불러오기
loader = PyPDFLoader("../../data/notice.pdf")
docs = loader.load()

# 로딩 결과 검증
validate(docs)