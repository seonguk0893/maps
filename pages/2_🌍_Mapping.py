import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="교통민원 데이터 지도 시각화",layout="wide", page_icon="🌍")

col1, col2, col3 = st.columns([1,5,2])
with col2:
    
    st.markdown("# 교통민원 데이터 지도 시각화")

    # st.write(
    #     """selectbox 위젯을 선택하여 교통민원 데이터를 구글맵에서 확인하실 수 있습니다."""
    # )


    # CSV 파일 딕셔너리 (키: 사용자가 보게 될 이름, 값: 실제 파일 경로)
    # csv_files = {"신호위반":"/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/신호위반.csv","불법유턴": "/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/불법유턴.csv", "진로 변경방법 위반":"/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/진로변경방법위반.csv", "꼬리물기": "/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/꼬리물기.csv", "불법좌회전":"/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/불법좌회전.csv","역주행":"/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/역주행.csv","정지선침범":"/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/정지선침범.csv","중앙선침범":"/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/중앙선침범.csv","지정차로위반":"/Users/ksy/문서/공모전/제3회_민원데이터분석경진대회/data/제3회민원데이터분석경진대회_모의데이터/csv/지정차로위반.csv"}

    data = pd.read_csv("./민원데이터_전체통합_주소완료_1003.csv")

    # Streamlit selectbox 위젯으로 CSV 파일 선택하기
    selected_csv_name = st.selectbox("Select a dataset:",data['신고유형'].unique())


    # 선택된 CSV 파일에서 데이터 로드 (위도와 경도 열이 '위도', '경도'인 경우)


    # # NaN 값 제거 

    data = data.fillna('NaN')

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["경도", "위도"],  # 주의: pydeck에서는 [경도, 위도] 순서로 입력합니다.
        get_color=[200, 30, 0, 160],
        get_radius=100,
    )

    view_state = pdk.ViewState(
        latitude=data["위도"].mean(),
        longitude=data["경도"].mean(),
        zoom=6,
        pitch=0,
    )

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(r)
