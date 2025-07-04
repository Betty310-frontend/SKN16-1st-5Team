import math
import pandas as pd
import streamlit as st
from streamlit_antd_components import pagination


# -------------------- FAQ 함수 --------------------
def show_faq(selected_maker):
    def load_faq(file_path, maker_name):
        df = pd.read_csv(file_path)
        df = df.rename(columns={"질문": "question", "답변": "answer"})
        df["maker"] = maker_name

        if maker_name == "Benz":
            df["topic"] = "없음"
        elif "카테고리" in df.columns:
            df = df.rename(columns={"카테고리": "topic"})
        else:
            df["topic"] = "기타"

        return df[["maker", "topic", "question", "answer"]]

    @st.cache_data
    def load_all_data():
        FILE_PATH = "docs"
        # FILE_PATH = "/content/drive/MyDrive/5조"
        df_benz = load_faq(f"{FILE_PATH}/benz_faq.csv", "Benz")
        df_genesis = load_faq(f"{FILE_PATH}/genesis_faq.csv", "Genesis")
        df_kia = load_faq(f"{FILE_PATH}/kia_faq.csv", "KIA")
        return pd.concat([df_benz, df_genesis, df_kia], ignore_index=True)

    faq_data = load_all_data()
    faq_data.insert(0, "index", range(1, len(faq_data) + 1))

    maker_data = faq_data[faq_data["maker"] == selected_maker]
    st.subheader(f"{selected_maker} FAQ")

    if selected_maker == "Benz":
        topic = "없음"
        search = st.text_input("검색어 입력", placeholder="검색어를 입력하세요.")
    else:
        col1, col2 = st.columns([2, 6])
        with col1:
            topic_list = ["전체"] + sorted(maker_data["topic"].unique())
            topic = st.selectbox("분류 선택", topic_list)
        with col2:
            search = st.text_input("검색어 입력", placeholder="검색어를 입력하세요.")

    filtered = maker_data.copy()
    if selected_maker != "Benz" and topic != "전체":
        filtered = filtered[filtered["topic"] == topic]
    if search:
        filtered = filtered[
            filtered["question"].str.contains(search, case=False, na=False)
        ]

    PAGE_SIZE = 10
    total = len(filtered)
    total_pages = math.ceil(total / PAGE_SIZE)

    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    start = (st.session_state.current_page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    current_data = filtered.iloc[start:end]

    st.divider()
    if not current_data.empty:
        for _, row in current_data.iterrows():
            with st.expander(f"Q. {row['question']}"):
                st.markdown(f"A. {row['answer']}")
    else:
        st.info("조건에 맞는 질문이 없습니다.")

    st.divider()
    col = st.columns([1, 2, 1])[1]
    with col:
        new_page = pagination(
            total=total, page_size=PAGE_SIZE, align="center", show_total=False
        )
        st.markdown(
            f"<p style='text-align:center;'>페이지 {new_page} / {total_pages}</p>",
            unsafe_allow_html=True,
        )

    if new_page != st.session_state.current_page:
        st.session_state.current_page = new_page
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()
