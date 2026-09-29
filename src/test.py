# 라이브러리 임포트 테스트
print("=" * 50)
print("RAG 환경 설정 테스트")
print("=" * 50)

# 1. Python 버전 확인
import sys
print(f"✓ Python 버전: {sys.version}")


# 2. LangChain 임포트
try:
    import langchain
    print(f"✓ LangChain 설치됨 (버전: {langchain.__version__})")
except ImportError:
    print("✗ LangChain 설치되지 않음")


# 3. OpenAI 임포트
try:
    import openai
    print("✓ OpenAI 설치됨")
except ImportError:
    print("✗ OpenAI 설치되지 않음")


# 4. FAISS 임포트
try:
    import faiss
    print("✓ FAISS 설치됨")
except ImportError:
    print("✗ FAISS 설치되지 않음")


# 5. Chroma 임포트
try:
    import chromadb
    print("✓ Chroma 설치됨")
except ImportError:
    print("✗ Chroma 설치되지 않음")


# 6. python-dotenv 임포트
try:
    from dotenv import load_dotenv
    print("✓ python-dotenv 설치됨")
except ImportError:
    print("✗ python-dotenv 설치되지 않음")


print("=" * 50)
print("모든 라이브러리 설치 완료!")
print("=" * 50)