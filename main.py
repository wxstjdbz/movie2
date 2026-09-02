import pandas as pd
import plotly.express as px
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "1년간 박스오피스 10위권에 든 영화 가운데 이 기간에 개봉한 216편의 요약표"
)


@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_URL,
        dtype={
            "movieCd": str,
            "openDt": str,
        },
    )

    # 여러 장르가 "|"로 구분된 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|", n=1)
        .str[0]
        .str.strip()
        .replace("", "미상")
    )

    return df


# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오지 못했습니다.")
    st.exception(e)
    st.stop()


# 숫자형 데이터 변환
numeric_cols = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ============================================================
# 1. 장르별 영화 편수
# ============================================================

st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="편수")
)

fig = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.5,
    title="장르별 영화 편수",
)

fig.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    ),
)

fig.update_layout(
    legend_title_text="장르",
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig, use_container_width=True)


# 그래프 설명 영역
with st.container(border=True):
    st.subheader("이 그래프로 알 수 있는 것")

    st.text_input(
        "한 문장으로 정리해 보세요.",
        placeholder="예: 가장 많은 장르는 ○○이고 전체 영화의 약 ○○%를 차지한다.",
        key="genre_insight",
        label_visibility="collapsed",
    )


st.divider()


# ============================================================
# 이후 그래프를 추가할 수 있는 공간
# ============================================================

st.header("2. 다음 그래프")

st.write(
    "여기에 다음 분석 그래프를 추가할 수 있습니다."
)
