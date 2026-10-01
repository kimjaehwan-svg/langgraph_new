# ============================================================
# Streamlit 기반 RAG 웹 애플리케이션
#
# 사용자의 질문을 입력받아 RAG 시스템에 전달하고
# 답변과 참고 문서를 대화형 화면으로 보여줍니다.
# ============================================================

import streamlit as st

import config
from rag import ask


# ============================================================
# 1. Streamlit 기본 설정
# ============================================================

st.set_page_config(
    page_title="문서 기반 RAG Q&A",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. 화면 디자인
# ============================================================

st.markdown(
    """
    <style>

    /* 전체 화면 최대 폭 */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* 제목 */
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    /* 부제목 */
    .sub-title {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* 문서 정보 박스 */
    .document-box {
        padding: 0.9rem 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }

    /* 출처 박스 */
    .source-box {
        padding: 0.7rem 0.9rem;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }

    /* 하단 설명 */
    .footer-text {
        color: #9ca3af;
        font-size: 0.8rem;
        text-align: center;
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. Session State 준비
# ============================================================

# 대화 기록
if "history" not in st.session_state:
    st.session_state.history = []

# 예제 질문을 클릭했을 때 사용할 값
if "example_question" not in st.session_state:
    st.session_state.example_question = None


# ============================================================
# 4. Sidebar
# ============================================================

with st.sidebar:

    st.header("⚙️ RAG 설정")

    st.markdown("##### 📄 현재 문서")

    st.code(
        config.DOC_PATH.name,
        language=None
    )

    st.divider()

    st.markdown("##### 문서 분할")

    st.write(
        f"**Chunk Size** : {config.CHUNK_SIZE}"
    )

    st.write(
        f"**Chunk Overlap** : "
        f"{config.CHUNK_OVERLAP}"
    )

    st.divider()

    st.markdown("##### 검색")

    st.write(
        f"**Top-K** : {config.TOP_K}"
    )

    st.write(
        f"**Minimum Score** : "
        f"{config.MIN_SCORE}"
    )

    st.divider()

    st.markdown("##### 생성 모델")

    st.write(
        f"**LLM** : {config.LLM_MODEL}"
    )

    st.write(
        f"**Prompt** : "
        f"{config.PROMPT_VER.upper()}"
    )

    st.divider()

    # --------------------------------------------------------
    # 새 대화 버튼
    # --------------------------------------------------------

    if st.button(
        "🗑️ 새 대화 시작",
        use_container_width=True
    ):

        st.session_state.history = []

        st.rerun()


# ============================================================
# 5. 메인 제목
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📘 문서 기반 RAG 질의응답'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'PDF 문서를 검색한 뒤, '
    '찾은 내용을 근거로 답변합니다.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 6. 현재 검색 문서 표시
# ============================================================

st.markdown(
    f"""
    <div class="document-box">
        📄 <b>현재 검색 문서</b><br>
        {config.DOC_PATH.name}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 7. 예제 질문
# ============================================================

# 대화가 아직 없을 때만 보여줍니다.
if len(st.session_state.history) == 0:

    st.markdown("#### 💡 이런 질문을 해보세요")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "대회의실은 몇 명까지 이용할 수 있나요?",
            use_container_width=True
        ):
            st.session_state.example_question = (
                "대회의실은 몇 명까지 "
                "이용할 수 있나요?"
            )

        if st.button(
            "예약은 언제까지 신청해야 하나요?",
            use_container_width=True
        ):
            st.session_state.example_question = (
                "예약은 언제까지 신청해야 하나요?"
            )

    with col2:

        if st.button(
            "예약 취소 시 환불 기준을 알려주세요.",
            use_container_width=True
        ):
            st.session_state.example_question = (
                "예약 취소 시 환불 기준을 "
                "알려주세요."
            )

        if st.button(
            "센터 주차요금은 얼마인가요?",
            use_container_width=True
        ):
            st.session_state.example_question = (
                "센터 주차요금은 얼마인가요?"
            )


# ============================================================
# 8. 기존 대화 기록 출력
# ============================================================

for question, result in st.session_state.history:

    # --------------------------------------------------------
    # 사용자 질문
    # --------------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(question)


    # --------------------------------------------------------
    # AI 답변
    # --------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="📘"
    ):

        # 오류 여부 확인
        if result.get("ok") is False:

            st.error(
                result["answer"]
            )

        else:

            st.write(
                result["answer"]
            )


        # ----------------------------------------------------
        # 출처 출력
        # ----------------------------------------------------

        sources = result.get(
            "sources",
            []
        )

        if sources:

            # 중복 출처 제거
            unique_sources = []

            seen = set()

            for source in sources:

                filename = source.get(
                    "file",
                    "unknown"
                )

                page = source.get(
                    "page",
                    "?"
                )

                key = (
                    filename,
                    page
                )

                if key not in seen:

                    seen.add(key)

                    unique_sources.append(
                        {
                            "file": filename,
                            "page": page
                        }
                    )


            # ----------------------------------------------
            # 출처 영역
            # ----------------------------------------------

            with st.expander(
                "📚 참고 자료",
                expanded=False
            ):

                for source in unique_sources:

                    st.markdown(
                        f"""
                        <div class="source-box">
                        📄 <b>{source["file"]}</b>
                        &nbsp;&nbsp;
                        📍 {source["page"]}페이지
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


            # ----------------------------------------------
            # 한 줄 출처 표시
            # ----------------------------------------------

            pages = []

            for source in unique_sources:

                page = source["page"]

                if page not in pages:
                    pages.append(page)


            try:
                pages.sort()

            except TypeError:
                pass


            page_text = ", ".join(
                str(page)
                for page in pages
            )


            filename = (
                unique_sources[0]["file"]
            )


            st.caption(
                f"📎 출처: "
                f"{filename} / "
                f"{page_text}페이지"
            )


        # ----------------------------------------------------
        # 인용 상태 표시
        # ----------------------------------------------------

        cited = result.get(
            "cited"
        )

        if cited is True:

            st.caption(
                "✓ 문서 근거 인용 확인"
            )

        elif cited is False:

            st.warning(
                "답변에 문서 인용 번호가 "
                "확인되지 않았습니다."
            )


# ============================================================
# 9. 사용자 질문 입력
# ============================================================

question = st.chat_input(
    "문서에 대해 궁금한 내용을 질문하세요."
)


# ============================================================
# 10. 예제 질문 처리
# ============================================================

if (
    st.session_state.example_question
    is not None
):

    question = (
        st.session_state.example_question
    )

    st.session_state.example_question = None


# ============================================================
# 11. 새로운 질문 처리
# ============================================================

if question:

    # --------------------------------------------------------
    # 사용자 질문 즉시 표시
    # --------------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(question)


    # --------------------------------------------------------
    # RAG 검색 및 답변 생성
    # --------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="📘"
    ):

        with st.spinner(
            "문서를 검색하고 답변을 "
            "생성하고 있습니다..."
        ):

            result = ask(question)


    # --------------------------------------------------------
    # 대화 기록 저장
    # --------------------------------------------------------

    st.session_state.history.append(
        (
            question,
            result
        )
    )


    # --------------------------------------------------------
    # 화면 다시 실행
    # --------------------------------------------------------

    st.rerun()


# ============================================================
# 12. 하단 안내
# ============================================================

st.markdown(
    """
    <div class="footer-text">
    RAG Practice ·
    문서 검색 결과를 바탕으로 답변합니다.
    </div>
    """,
    unsafe_allow_html=True
)