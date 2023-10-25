import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import branca
from folium import Icon
from folium import plugins
from branca.element import Template, MacroElement


# Streamlit 애플리케이션 제목
st.set_page_config(page_title="교통민원 및 사고 정보 시각화",layout="wide", page_icon="🗺️")


sido_options = ["선택","서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",  "경기도", "강원특별자치도",
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
    "강원특별자치도": ["선택", "강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군", "원주시", "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군", "횡성군"],
    "충청북도": ["선택", "괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "제천시", "증평군", "진천군", "청주시", "충주시"],
    "충청남도": ["선택", "계룡시", "공주시", "금산군", "논산시", "당진시", "보령시", "부여군", "서산시", "서천군", "아산시", "예산군", "천안시", "청양군", "태안군", "홍성군"],
    "전라북도": ["선택", "고창군", "군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "임실군", "장수군", "전주시", "정읍시", "진안군"],
    "전라남도": ["선택", "강진군", "고흥군", "곡성군", "광양시", "구례군", "나주시", "담양군", "목포시", "무안군", "보성군", "순천시", "신안군", "여수시", "영광군", "영암군", "완도군", "장성군", "장흥군", "진도군", "함평군", "해남군", "화순군"],
    "경상북도": ["선택", "경산시", "경주시", "고령군", "구미시", "군위군", "김천시", "문경시", "봉화군", "상주시", "성주군", "안동시", "영덕군", "영양군", "영주시", "영천시", "예천군", "울릉군", "울진군", "의성군", "청도군", "청송군", "칠곡군"],
    "경상남도": ["선택", "거제시", "거창군", "고성군", "김해시", "남해군", "밀양시", "사천시", "산청군", "양산시", "의령군", "진주시", "창녕군", "창원시", "통영시", "하동군", "함안군", "함양군", "합천군"],
    "제주특별자치도": ["선택", "서귀포시", "제주시"]
}




#sido = st.sidebar.radio("시도명을 선택하세요", sido_options)

col1, col2, col3 = st.columns([1,5,2])
with col2:
    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<b><p class="big-font">시도-시군별 민원 정보 및 사고 정보 Map</p></b>', unsafe_allow_html=True)
    
    col4,col5 = st.columns([1,1])
    with col4:
        sido = st.selectbox("시도명을 선택하세요", sido_options)
        sigun = sigun_list.get(sido, [])
    with col5:
        select_sigun = st.selectbox("시군구를 선택하세요", sigun)
        

    # CSV 파일 업로드
    #uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

    # 사용자가 시도명을 입력한 경우
    #user_sido = st.text_input("시도명을 입력하세요")

    #if uploaded_file is not None:
        # CSV 파일 읽기
    df = pd.read_csv("./민원데이터_전체통합_주소완료_1003.csv")
    df1 = pd.read_csv("./민원포함_긍부정요인완료_1017.csv")

    #initial_location = [df['위도'].mean(), df['경도'].mean()]
    initial_location = [36.13,128.11]


        # 지도 초기화
    m = folium.Map(location=initial_location, tiles="cartodbpositron", zoom_start=7)
    bounds = []  # 마커의 경계를 저장할 리스트

    # 라디오 버튼로 시도 선택


        # 사용자가 시도명을 입력한 경우
    if sido != "선택":
        selected_rows = df[(df['시도명'] == sido) & (df['시군구명'] == select_sigun)]
        selected_rows1 = df1[(df1['시군구_시도명'] == sido) & (df1['시군구_시군명'] == select_sigun)]
        if select_sigun != "선택":
            selected_rows = selected_rows[selected_rows['시군구명'] == select_sigun]

        
        if not selected_rows.empty:
            st.write(f"{sido} {select_sigun}의 위치를 지도에 표시합니다.")
            tw = df1['traffic_weight'].mean()
            tw1 = selected_rows1['traffic_weight'].mean()
            most_common_type = selected_rows['신고유형'].mode().iloc[0]
            
            all_top_values = []

            # 다섯 개의 열에 대해 각각 가장 많이 나온 3가지 값을 찾아 리스트에 추가
            for i in range(1, 6):
                column_name = f'교통사고_위험인자_{i}'
                top_values = selected_rows1[column_name].value_counts().index[0:3]
                all_top_values.extend(top_values)

            # 리스트에서 가장 많이 나온 5가지 값을 찾음
            top_5 = pd.Series(all_top_values).value_counts().index[0:5].values
            
            # 가장 많은 신고유형 출력
            st.markdown(f'{sido} {select_sigun} 민원 신고 건수 : <b>{len(selected_rows)}</b>', unsafe_allow_html=True)
            st.markdown(f'{sido} {select_sigun}에서 가장 많은 신고유형은 <span style="color: black;"></span> <span style="color: #FF0000;"><b>{most_common_type}</b></span> 입니다. (빨간색으로 표시)', unsafe_allow_html=True)
            st.markdown(f'전국 사고 위험지수 평균 : <span style="color: #FF0000;"><b>{tw}</b></span>', unsafe_allow_html=True)
            if tw > tw1:
                st.markdown(f'{sido} {select_sigun}의 사고 위험지수 평균은 <span style="color: black;"></span> <span style="color: #FF0000;"><b>{tw1}</b></span> 로 전국 평균보다 낮습니다.', unsafe_allow_html=True)
            else:
                st.markdown(f'{sido} {select_sigun}의 사고 위험지수 평균은 <span style="color: black;"></span> <span style="color: #FF0000;"><b>{tw1}</b></span> 로 전국 평균보다 높습니다.', unsafe_allow_html=True)
                
            st.markdown(f'{sido} {select_sigun}에서 가장 영향을 끼친 사고요인 top 5<br><b>{top_5}</b>', unsafe_allow_html=True)
            

            for index, row in selected_rows.iterrows():
                latitude = row['위도']
                longitude = row['경도']
                address1 = row['시도명']
                address2 = row['ADDRESS']
                type_s = row['신고유형']

                    # 지도에 해당 위치의 마커 추가
                html = """<!DOCTYPE html>
                                    <html>
                                        <table style="height: 126px; width: 330px;">  <tbody> <tr>
                                        <td style="background-color: #ab60f0;"><div style="color: #ffffff;text-align:center;">주소</div></td>
                                        <td style="width: 200px;background-color: #D3D3D3;">{}</td>""".format(address2) + """ </tr> 
                                        <tr><td style="background-color: #ab60f0;"><div style="color: #ffffff;text-align:center;">신고유형</div></td>
                                        <td style="width: 200px;background-color: #D3D3D3;">{}</td>""".format(type_s) + """</tr>
                                        <tr><td style="background-color: #ab60f0;"><div style="color: #ffffff;text-align:center;">발생일</div></td>
                                        <td style="width: 200px;background-color: #D3D3D3;">{}</td>""".format(row['발생일']) + """ </tr>
                                    </tbody> </table> </html> """


                iframe = branca.element.IFrame(html=html, width=350, height=150)
                popup_text = folium.Popup(iframe, parse_html=True)
                
                def set_marker_color(type_s):
                    if type_s == most_common_type:
                        return "red"
                    else:
                        return "blue"
                    
#                 accident_type_colors = {
#                     "진로변경방법위반": "red",
#                     "신호위반": "blue",
#                     "불법좌회전": "green",
#                     "중앙선침범": "purple",
#                     "정지선침범": "orange",
#                     "불법유턴": "pink",
#                     "지정차로위반": "yellow",
#                     "역주행": "cyan",
#                     "꼬리물기": "magenta",
#                 }

#                 # set_marker_color 함수를 수정하여 신고유형에 따라 색상을 반환하도록 합니다
#                 def set_marker_color(type_s):
#                     return accident_type_colors.get(type_s, "blue")
                
                marker_color = set_marker_color(type_s)
                
                # 마커 아이콘 설정
                icon = plugins.BeautifyIcon(icon="dot", icon_size=(8, 8), border_color=marker_color, text_color=marker_color)
                
                
                #icon = plugins.BeautifyIcon(icon="dot", icon_size=(8, 8), border_color="blue", text_color="blue")


                folium.Marker([latitude, longitude], icon=icon, popup=popup_text, tooltip=row['ADDRESS']).add_to(m)
                bounds.append([latitude, longitude])  # 경계에 추가

                # 경계 상자 설정 및 지도 이동
            if bounds:
                m.fit_bounds(bounds)

        else:
            st.warning("해당 지역은 CSV파일에 데이터가 없습니다.", icon="⚠️")

        # Streamlit Folium을 사용하여 지도를 표시
    st_folium(m, width=1000)
