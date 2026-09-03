import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# 페이지 설정
# =========================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide"
)


# =========================================================
# 데이터 불러오기
# =========================================================
URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

df = pd.read_csv(URL)

# 장르가 여러 개라면 첫 번째 장르만 사용
df["genre"] = (
    df["genre"]
    .fillna("기타")
    .astype(str)
    .str.split("|")
    .str[0]
)

# 국가 결측값 처리
df["nation"] = df["nation"].fillna("기타")

# 숫자형 데이터 변환
number_cols = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for col in number_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 필요한 데이터가 없는 행 제거
df = df.dropna(
    subset=["movieNm", "genre", "total_audi"]
)


# =========================================================
# 제목
# =========================================================
st.title("🎬 영화 데이터 그래프 도감 2")
st.subheader("분포와 관계를 그래프로 살펴보는 영화 데이터 분석")

st.write("")


# =========================================================
# 기본 통계
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎞️ 전체 영화 수", f"{len(df):,}편")

with col2:
    st.metric("🎭 장르 수", f"{df['genre'].nunique()}개")

with col3:
    st.metric("🌏 제작 국가 수", f"{df['nation'].nunique()}개")

st.divider()


# =========================================================
# GRAPH 01
# 장르별 영화 수
# =========================================================
st.header("🎭 1. 장르별 영화 수")

st.write(
    "어떤 장르의 영화가 가장 많이 포함되어 있는지 확인해 봅니다."
)

genre_count = df["genre"].value_counts().reset_index()
genre_count.columns = ["genre", "count"]

fig1 = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.45
)

fig1.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    height=500,
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.info("💡 이 그래프로 알 수 있는 것")

st.text_input(
    "장르 분포에 대한 한 문장 해석을 작성해 보세요.",
    key="interpretation_1"
)

st.divider()


# =========================================================
# GRAPH 02
# 장르 → 영화 트리맵
# =========================================================
st.header("🌳 2. 장르별 흥행 규모")

st.write(
    "타일의 크기가 클수록 누적 관객 수가 많은 영화입니다."
)

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "누적 관객 수: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=600,
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.info("💡 이 그래프로 알 수 있는 것")

st.text_input(
    "장르별 흥행 규모에 대한 한 문장 해석을 작성해 보세요.",
    key="interpretation_2"
)

st.divider()


# =========================================================
# GRAPH 03
# 누적 관객 수 히스토그램
# =========================================================
st.header("📊 3. 누적 관객 수 분포")

st.write(
    "영화들의 누적 관객 수가 어느 구간에 가장 많이 몰려 있는지 확인합니다."
)

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    labels={
        "total_audi": "누적 관객 수"
    }
)

fig3.update_layout(
    height=500,
    xaxis_title="누적 관객 수",
    yaxis_title="영화 수",
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# 가장 영화가 많이 몰린 구간
hist_counts, bin_edges = np.histogram(
    df["total_audi"].dropna(),
    bins=20
)

max_bin_index = hist_counts.argmax()

bin_start = bin_edges[max_bin_index]
bin_end = bin_edges[max_bin_index + 1]

# 가장 많은 관객을 모은 영화
highest_movie_row = df.loc[
    df["total_audi"].idxmax()
]

highest_movie = highest_movie_row["movieNm"]
highest_audience = highest_movie_row["total_audi"]

st.success(
    f"📌 가장 영화가 많이 몰린 관객 구간: "
    f"약 {bin_start:,.0f}명 ~ {bin_end:,.0f}명"
)

st.success(
    f"🏆 가장 많은 관객을 모은 영화: "
    f"{highest_movie} — {highest_audience:,.0f}명"
)

st.info("💡 이 그래프로 알 수 있는 것")

st.text_input(
    "관객 수 분포에 대한 한 문장 해석을 작성해 보세요.",
    key="interpretation_3"
)

st.divider()


# =========================================================
# GRAPH 04
# 스크린 수 vs 누적 관객 수
# =========================================================
st.header("📈 4. 스크린 수와 누적 관객 수의 관계")

st.write(
    "개봉 당시 스크린 수가 많을수록 최종 관객 수도 많아지는지 살펴봅니다."
)

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={
        "first_scrn": "개봉 첫날 스크린 수",
        "total_audi": "누적 관객 수",
        "genre": "장르"
    }
)

fig4.update_layout(
    height=600,
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.info("💡 이 그래프로 알 수 있는 것")

st.text_input(
    "스크린 수와 관객 수의 관계에 대한 한 문장 해석을 작성해 보세요.",
    key="interpretation_4"
)

st.divider()


# =========================================================
# GRAPH 05
# 장르별 관객 수 박스플롯
# =========================================================
st.header("📦 5. 장르별 관객 수 분포 비교")

st.write(
    "영화가 10편 이상 있는 장르만 골라 장르별 관객 수의 차이를 비교합니다."
)

genre_10 = df["genre"].value_counts()

valid_genres = genre_10[
    genre_10 >= 10
].index

box_df = df[
    df["genre"].isin(valid_genres)
]

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    labels={
        "genre": "장르",
        "total_audi": "누적 관객 수"
    }
)

fig5.update_layout(
    height=600,
    showlegend=False,
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.info("💡 이 그래프로 알 수 있는 것")

st.text_input(
    "장르별 관객 분포에 대한 한 문장 해석을 작성해 보세요.",
    key="interpretation_5"
)

st.divider()


# =========================================================
# GRAPH 06
# 버블 차트
# =========================================================
st.header("🫧 6. 스크린 수 · 누적 관객 · 첫 주 관객")

st.write(
    "스크린 수와 누적 관객 수의 관계를 보면서 "
    "버블 크기로 첫 주 관객 수까지 함께 비교합니다."
)

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "first_scrn": ":,",
        "first_week_audi": ":,",
        "total_audi": ":,",
        "genre": True
    },
    labels={
        "first_scrn": "개봉 첫날 스크린 수",
        "total_audi": "누적 관객 수",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르"
    },
    size_max=55
)

fig6.update_layout(
    height=650,
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.info("💡 이 그래프로 알 수 있는 것")

st.text_input(
    "첫 주 관객과 최종 흥행에 대한 한 문장 해석을 작성해 보세요.",
    key="interpretation_6"
)

st.divider()


# =========================================================
# GRAPH 07
# 국가 → 장르 선버스트
# =========================================================
st.header("🌏 7. 제작 국가와 장르의 관계")

st.write(
    "어느 국가의 영화가 어떤 장르로 많이 만들어졌는지 한눈에 살펴봅니다."
)

fig7 = px.sunburst(
    df,
    path=["nation", "genre"]
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    height=650,
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.info("💡 이 그래프로 알 수 있는 것")

st.text_input(
    "제작 국가와 장르의 관계에 대한 한 문장 해석을 작성해 보세요.",
    key="interpretation_7"
)

st.divider()


# =========================================================
# GRAPH 08
# 첫 주 흥행 비중 분석
# =========================================================
st.header("🔥 8. 첫 주 흥행 비중과 최종 흥행")

st.write(
    "개봉 첫 주에 최종 관객의 몇 %를 모았는지 비교합니다. "
    "첫 주 비중이 높을수록 초반에 관객이 집중된 영화라고 볼 수 있습니다."
)

# 분석용 데이터 만들기
analysis_df = df[
    (df["total_audi"] > 0) &
    (df["first_week_audi"].notna())
].copy()

# 첫 주 관객 비중 계산
analysis_df["first_week_ratio"] = (
    analysis_df["first_week_audi"]
    / analysis_df["total_audi"]
    * 100
)

# 정상 범위의 값만 사용
analysis_df = analysis_df[
    analysis_df["first_week_ratio"].between(0, 100)
]

# 그래프
fig8 = px.scatter(
    analysis_df,
    x="first_week_ratio",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "first_week_ratio": ":.1f",
        "first_week_audi": ":,",
        "total_audi": ":,",
        "genre": True
    },
    labels={
        "first_week_ratio": "첫 주 관객 비중 (%)",
        "total_audi": "누적 관객 수",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르"
    }
)

fig8.update_layout(
    height=650,
    xaxis_title="첫 주 관객 비중 (%)",
    yaxis_title="누적 관객 수",
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(
    fig8,
    use_container_width=True
)


# =========================================================
# GRAPH 08 분석 결과
# =========================================================
if len(analysis_df) > 0:

    highest_ratio_row = analysis_df.loc[
        analysis_df["first_week_ratio"].idxmax()
    ]

    lowest_ratio_row = analysis_df.loc[
        analysis_df["first_week_ratio"].idxmin()
    ]

    average_ratio = analysis_df["first_week_ratio"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📊 평균 첫 주 관객 비중",
            f"{average_ratio:.1f}%"
        )

    with col2:
        st.metric(
            "🚀 가장 높은 영화",
            highest_ratio_row["movieNm"],
            f"{highest_ratio_row['first_week_ratio']:.1f}%"
        )

    with col3:
        st.metric(
            "🌱 가장 낮은 영화",
            lowest_ratio_row["movieNm"],
            f"{lowest_ratio_row['first_week_ratio']:.1f}%"
        )

else:
    st.warning(
        "첫 주 관객 수와 누적 관객 수를 이용할 수 있는 데이터가 없습니다."
    )


st.info("💡 이 그래프로 알 수 있는 것")

st.text_input(
    "첫 주 흥행 비중에 대한 한 문장 해석을 작성해 보세요.",
    key="interpretation_8"
)

st.divider()


# =========================================================
# 마무리
# =========================================================
st.success(
    "🎉 분석 완료! "
    "총 8개의 그래프를 통해 영화 데이터를 여러 관점에서 살펴보았습니다."
)

st.write(
    "🎭 장르 분포  ·  "
    "🌳 장르별 흥행 규모  ·  "
    "📊 관객 수 분포  ·  "
    "📈 스크린 수와 관객 수의 관계  ·  "
    "📦 장르별 관객 분포  ·  "
    "🫧 첫 주 관객과 최종 관객의 관계  ·  "
    "🌏 국가와 장르의 관계  ·  "
    "🔥 첫 주 흥행 비중과 최종 흥행"
)
