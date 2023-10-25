from streamlit_extras.dataframe_explorer import dataframe_explorer 



from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st

st.set_page_config(page_title="데이터 프레임 자동 필터링 시각화",layout="wide", page_icon="🔭")

col1, col2, col3 = st.columns([1,5,2])
with col2:

    def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        뷰어가 열을 필터링할 수 있도록 데이터 프레임 위에 UI를 추가합니다.


        Args:
            df (pd.DataFrame): 원본 데이터프레임

        Returns:
            pd.DataFrame: 필터링된 데이터프레임
        """
        modify = st.checkbox("Add filters")

        if not modify:
            return df

        # 사용자 입력으로 인해 기본 데이터가 변경되지 않도록 pandas 데이터프레임의 복사본을 만듬
        df = df.copy()

        # 표준 형식(날짜 시간, 표준 시간대 없음)으로 날짜 시간을 변환
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        modification_container = st.container()

        # 이 함수에서는 세 가지 pandas 데이터 유형(범주형, 숫자형, 날짜/시간)을 확인한 다음 나머지를 문자열인 것처럼 처리하려고 합니다. 
        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                # Treat columns with < 10 unique values as categorical
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]
                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"Values for {column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                else:
                    user_text_input = right.text_input(
                        f"Substring or regex in {column}",
                    )
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input)]

        return df

    st.title("🔭데이터 프레임 자동 필터링 시각화")
    st.write(
        """데이터 프레임에 대해 세세한 필터링을 넣으실 수 있습니다!                        
        다양한 조건을 통해 원하시는 교통사고 민원 데이터를 찾아보세요 >_ㅇ
        """
    )



    #data_url = "./민원포함_긍부정요인완료_1017.csv"

    df = pd.read_csv("./전국_교통사고_민원포함_긍부정요인완료_1017.csv")
    st.dataframe(filter_dataframe(df))

    # 데이터 프레임 자동 필터링 UI 구현