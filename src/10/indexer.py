from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PREPARE_DIR = os.path.join(CURRENT_DIR, "..", "07")
sys.path.insert(0, PREPARE_DIR)
from prepare import prepare_chunks

load_dotenv()

DOC_PATH = "../../data/manual.pdf"
INDEX_PATH = "faiss_index"
EMBED_MODEL = "text-embedding-3-small"

def get_store(rebuild=False):
    emb = OpenAIEmbeddings(model="text-embedding-3-small")

    if os.path.exists(INDEX_PATH) and not rebuild:
        store = FAISS.load_local(
            INDEX_PATH,
            emb,
            allow_dangerous_deserialization=True
        )
        return store

    chunks = prepare_chunks(DOC_PATH)

    store = FAISS.from_documents(
        chunks,
        emb
    )

    store.save_local(INDEX_PATH)
    print("저장 완료")

    return store

if __name__ == "__main__":
    store = get_store()


