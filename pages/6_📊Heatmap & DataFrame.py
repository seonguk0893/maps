import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import plugins
import branca
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm 
from matplotlib import font_manager, rc

font_fname = './NanumGothic.ttf'
font_family = font_manager.FontProperties(fname=font_fname).get_name()

plt.rcParams["font.family"] = font_family

st.set_page_config(page_title="히트맵 시각화",layout="wide", page_icon="📊")

# Define your province and city data
sido_options = ["선택","서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",  "경기도", "강원도",
                "충청북도", "충청남도", "전라북도", "전라남도", "경상북도",  "경상남도", "제주특별자치도"]

sigun_list = {
    "서울특별시": ["선택", "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    "부산광역시": ["선택", "강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
    "대구광역시": ["선택", "남구", "달서구", "달성군", "동구", "북구", "서구", "수성구", "중구"],
    "인천광역시": ["선택", "강화군", "계양구", "미추홀구", "남동구", "동구", "부평구", "서구", "연수구", "옹진군", "중구"],
    "광주광역시": ["선택", "광산구", "남구", "동구", "북구", "서구"],
    "대전광역시": ["선택", "대덕구", "동구", "서구", "유성구", "중구"],
    "울산광역시": ["선택", "남구", "동구", "북구", "울주군", "중구"],
    "세종특별자치시": ["선택", "세종시"],
    "경기도": ["선택", "가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"],
    "강원도": ["선택", "강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군", "원주시", "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군", "횡성군"],
    "충청북도": ["선택", "괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "제천시", "증평군", "진천군", "청주시", "충주시"],
    "충청남도": ["선택", "계룡시", "공주시", "금산군", "논산시", "당진시", "보령시", "부여군", "서산시", "서천군", "아산시", "예산군", "천안시", "청양군", "태안군", "홍성군"],
    "전라북도": ["선택", "고창군", "군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "임실군", "장수군", "전주시", "정읍시", "진안군"],
    "전라남도": ["선택", "강진군", "고흥군", "곡성군", "광양시", "구례군", "나주시", "담양군", "목포시", "무안군", "보성군", "순천시", "신안군", "여수시", "영광군", "영암군", "완도군", "장성군", "장흥군", "진도군", "함평군", "해남군", "화순군"],
    "경상북도": ["선택", "경산시", "경주시", "고령군", "구미시", "군위군", "김천시", "문경시", "봉화군", "상주시", "성주군", "안동시", "영덕군", "영양군", "영주시", "영천시", "예천군", "울릉군", "울진군", "의성군", "청도군", "청송군", "칠곡군"],
    "경상남도": ["선택", "거제시", "거창군", "고성군", "김해시", "남해군", "밀양시", "사천시", "산청군", "양산시", "의령군", "진주시", "창녕군", "창원시", "통영시", "하동군", "함안군", "함양군", "합천군"],
    "제주특별자치도": ["선택", "서귀포시", "제주시"]
}

df = pd.read_csv("./전국_월별_읍면동별_독립변인_법규위반_노면상태_기상상태_도로형태_완료_1006.csv")

col1, col2, col3 = st.columns([1,5,2])
with col2:

    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<b><p class="big-font">시도-시군별 교통사고위험지수 민원건수 상관관계</p></b>', unsafe_allow_html=True)
    
    col4,col5 = st.columns([1,1])
    with col4:
        selected_sido = st.selectbox("시도명을 선택하세요", sido_options)
        sigun = sigun_list.get(selected_sido, [])
    with col5:
        selected_sigun = st.selectbox("시군구를 선택하세요", sigun)


    # Filter the DataFrame based on the selected "시도" and "시군"
    filtered_df = df[(df['시군구_시도명'] == selected_sido) & (df['시군구_시군명'] == selected_sigun)]

    selected_columns = ['교통사고위험지수', '꼬리물기_건수', '불법유턴_건수', '불법좌회전_건수', '신호위반_건수', '역주행_건수', '정지선침범_건수', '중앙선침범_건수',
                        '지정차로위반_건수', '진로변경방법위반_건수', '민원_전체건수']


    # Create a subset of the DataFrame with only the selected columns
    filtered_df_subset = filtered_df[selected_columns]

    # Calculate the correlation matrix for the selected columns
    correlation_matrix = filtered_df_subset.corr()

    # Create a heatmap for the selected "시도" and "시군"
    st.write(f"## Heatmap for {selected_sido} {selected_sigun}")
    plt.figure(figsize=(10, 8))
    # sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5, fmt=".2f")
    # heatmap_figure = plt.gcf()  # Get the current figure

    # Display the figure using st.pyplot()
    # st.pyplot(heatmap_figure)
    plot = sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5, fmt=".2f")
 
    # 플롯을 Streamlit에 표시
    st.pyplot(plot.get_figure())

    # Display the filtered DataFrame with the selected columns
    st.write(f"## DataFrame for {selected_sido} {selected_sigun}")
    st.dataframe(filtered_df_subset)
