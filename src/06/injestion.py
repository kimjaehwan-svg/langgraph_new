import os
import re

from langchain_community.document_loaders import PyPDFLoader


NOISE = ["대외비"]


def load_documents(path: str):
    # 문서를 읽고, 정리하고, 검증까지 한 번에
    docs = PyPDFLoader(path).load()

    for d in docs:
        # 본문 정제
        text = d.page_content

        for n in NOISE:
            text = text.replace(n, "")

        text = re.sub(r"\n{3,}", "\n\n", text)
        d.page_content = text.strip()

        # metadata 보강
        d.metadata["filename"] = os.path.basename(path)
        d.metadata["page_no"] = d.metadata.get("page", 0) + 1

    # 검증
    empty = [
        d.metadata["page_no"]
        for d in docs
        if len(d.page_content) < 10
    ]

    if empty:
        print("내용이 없는 페이지:", empty)

    print(f"총 {len(docs)}쪽 로딩 완료")
    print(f"총 {sum(len(d.page_content) for d in docs)}자")

    return docs


if __name__ == "__main__":
    docs = load_documents("../../data/manual.pdf")

    print(docs[0].page_content[:200])