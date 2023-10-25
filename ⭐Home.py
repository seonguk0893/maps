import streamlit as st

# 외부 페이지 노출 시 표시되는 데이터
st.set_page_config(
    page_title="교통관련 데이터 시각화 갤러리",
    page_icon="🚘",
    initial_sidebar_state="expanded",
    layout="wide"
)

col1, col2, col3 = st.columns([1,5,2])
with col2:
    
    st.title("🚘교통관련 데이터 시각화 갤러리")
    st.markdown(
            """
    안녕하세요~~👋

    **교통사고 민원데이터 갤러리**에 오신 것을 환영합니다!

    왼쪽 사이드 바에서 다양한 시각화를 둘러보세요~!

    """
    )

    # st.sidebar.success("Select a demo above.")

    # st.markdown(
    #     """
    #     Streamlit is an open-source app framework built specifically for
    #     Machine Learning and Data Science projects.
    #     **👈 Select a demo from the sidebar** to see some examples
    #     of what Streamlit can do!
    #     ### Want to learn more?
    #     - Check out [streamlit.io](https://streamlit.io)
    #     - Jump into our [documentation](https://docs.streamlit.io)
    #     - Ask a question in our [community
    #         forums](https://discuss.streamlit.io)
    #     ### See more complex demos
    #     - Use a neural net to [analyze the Udacity Self-driving Car Image
    #         Dataset](https://github.com/streamlit/demo-self-driving)
    #     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    # """
    # )
    
