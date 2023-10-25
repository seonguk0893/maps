import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="교통민원 데이터 통계", layout="wide", page_icon="📈")


col1, col2, col3 = st.columns([1,5,2])
with col2:
    st.markdown("# 교통민원 데이터 통계 ")

    @st.cache_data  # 👈 Add the caching decorator
    def load_data(url):
        df = pd.read_csv(url)
        return df


    try:
        df = load_data("./민원포함_긍부정요인완료_1017.csv")

        # Select column to plot
        columns_to_plot= ["꼬리물기_민원건수","불법유턴_민원건수","불법좌회전_민원건수","신호위반_민원건수","역주행_민원건수","정지선침범_민원건수","중앙선침범_민원건수","지정차로위반_민원건수","진로변경방법위반_민원건수","민원_전체건수","법규위반_안전운전불이행_건수","법규위반_보행자보호의무위반_건수","법규위반_신호위반_건수","법규위반_교차로운행방법위반_건수","법규위반_중앙선침범_건수","법규위반_직진우회전진행방해_건수","법규위반_불법유턴_건수","법규위반_안전거리미확보_건수","법규위반_기타_건수","법규위반_차로위반_건수","노면상태_건조_건수","노면상태_서리결빙_건수","노면상태_젖음습기_건수","노면상태_적설_건수","노면상태_기타_건수","기상상태_맑음_건수","기상상태_흐림_건수","기상상태_비_건수","기상상태_안개_건수","기상상태_눈_건수","기상상태_기타_건수","도로형태_교차로안_건수","도로형태_교차로부근_건수","도로형태_교차로횡단보도내_건수","도로형태_교량_건수","도로형태_터널_건수","도로형태_지하차도_건수","도로형태_단일로_기타_건수","도로형태_주차장_건수"]
        selected_column = st.selectbox("Choose a column to plot", columns_to_plot)

        # 시작시 강원도를 default값으로 보여줌
        regions = st.multiselect(
            "Choose regions", list(df['시군구_시도명'].unique()), ["강원도"]
        )

        if not regions:
            st.error("Please select at least one region.")

        else:
            data = df[df['시군구_시도명'].isin(regions)]

            # 월을 숫자 형태로 바꾸기 위한 딕셔너리입니다.
            month_dict = {"1월": "01", "2월": "02", "3월": "03", 
                          "4월": "04", "5월": "05", "6월": "06",
                          "7월": "07", "8월": "08", "9월": "09",
                          "10월": "10", "11월": "11", "12월":"12"}

            # -0--
            df['사고일시_연도'] = df['사고일시_연도'].str.replace('년', '')
            df['사고일시_월'] = df['사고일시_월'].map(month_dict)

            # 사고일시 연도와 월 칼럼을 합쳐서 새로운 date 칼럼을 만듭니다.
            df['date'] = pd.to_datetime(df['사고일시_연도'] + '-' + df['사고일시_월'])

            # 필요한 칼럼만 선택합니다.
            data_to_plot = []


            for region in regions:
                data_region = df[df["시군구_시도명"] == region]


                data_region_grouped= data_region[['date',selected_column]].groupby('date').sum().reset_index()
                data_region_grouped["region"] = region

                data_to_plot.append(data_region_grouped)

            final_df_to_plot = pd.concat(data_to_plot)

            chart = (
                alt.Chart(final_df_to_plot)
                .mark_line()
                .encode(
                    x='date:T',
                    y=alt.Y(f'{selected_column}:Q', title=f'{selected_column}'),
                    color='region:N',
                    tooltip=['date', f'{selected_column}', 'region']
                )
                .interactive()
                .properties(
                    width=800,
                    height=400
                )
             )
            st.altair_chart(chart, use_container_width=True)
    except Exception as e:
         st.error(f"An error occurred: {e}")

