from langchain_community.document_loaders import PyPDFLoader


def validate(docs):
    # 전체 유효한지 확인
    print("수:", len(docs))
    print("전체 페이지")

    # 빈 페이지 체크 (내용 없으면 스캔본 의심)
    empty_pages = []

    for d in docs:
        text = d.page_content.strip()

        if len(text) < 10:
            empty_pages.append(d.metadata.get("page", "?"))

    if empty_pages:
        print("내용이 거의 없는 페이지:", empty_pages)
        print("스캔 PDF일 수 있습니다.")
    else:
        print("빈 페이지 없음")

    # 전체 글자 수 확인
    total_len = 0

    for d in docs:
        total_len += len(d.page_content)

    print("전체 글자 수:", total_len)

    # 첫 페이지 내용 일부 확인
    print("-" * 45)

    if docs:
        print("첫 페이지 내용:", docs[0].page_content[:200])

    print("-" * 45)


# PDF 파일 불러오기
loader = PyPDFLoader("../../data/notice.pdf")
docs = loader.load()

# 검증 함수 실행
validate(docs)