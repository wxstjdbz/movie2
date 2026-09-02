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

    # 제작 국가 결측값 처리
    df["nation"] = (
        df["nation"]
        .fillna("미상")
        .astype(str)
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

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.5,
    title="장르별 영화 편수",
)

fig1.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    ),
)

fig1.update_layout(
    legend_title_text="장르",
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig1, use_container_width=True)

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
# 2. 장르 → 영화 트리맵
# ============================================================

st.header("2. 장르 안에 들어 있는 영화")

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].dropna(subset=["movieNm", "total_audi"])

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객",
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig2, use_container_width=True)

with st.container(border=True):
    st.subheader("이 그래프로 알 수 있는 것")
    st.text_input(
        "한 문장으로 정리해 보세요.",
        placeholder="예: ○○ 장르에서 총 관객이 많은 영화들이 특히 크게 나타난다.",
        key="treemap_insight",
        label_visibility="collapsed",
    )


st.divider()


# ============================================================
# 3. 총 관객 히스토그램
# ============================================================

st.header("3. 총 관객 분포")

hist_df = df.dropna(subset=["total_audi"]).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객",
        "count": "영화 편수",
    },
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="총 관객",
    yaxis_title="영화 편수",
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig3, use_container_width=True)


# 가장 관객이 많은 영화
max_audience_row = df.loc[df["total_audi"].idxmax()]
max_movie = max_audience_row["movieNm"]
max_audience = max_audience_row["total_audi"]

# 가장 영화가 많이 몰린 구간 계산
counts, bin_edges = pd.cut(
    hist_df["total_audi"],
    bins=20,
    retbins=True,
    include_lowest=True,
)

bin_counts = counts.value_counts().sort_index()
most_common_bin = bin_counts.idxmax()

st.info(
    f"📊 **대부분의 영화가 몰려 있는 구간:** "
    f"{most_common_bin.left:,.0f}명 ~ {most_common_bin.right:,.0f}명\n\n"
    f"🏆 **가장 관객이 많은 영화:** "
    f"**{max_movie}** — 총 관객 {max_audience:,.0f}명"
)

with st.container(border=True):
    st.subheader("이 그래프로 알 수 있는 것")
    st.text_input(
        "한 문장으로 정리해 보세요.",
        placeholder="예: 대부분의 영화는 ○○만 명 이하 구간에 몰려 있으며, 가장 많은 관객을 모은 영화는 ○○이다.",
        key="histogram_insight",
        label_visibility="collapsed",
    )


st.divider()


# ============================================================
# 4. 개봉일 스크린수 × 총 관객 산점도
# ============================================================

st.header("4. 개봉일 스크린수와 총 관객의 관계")

scatter_df = df.dropna(
    subset=["first_scrn", "total_audi", "movieNm", "genre"]
).copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "genre": "장르",
    },
)

fig4.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig4, use_container_width=True)

with st.container(border=True):
    st.subheader("이 그래프로 알 수 있는 것")
    st.text_input(
        "한 문장으로 정리해 보세요.",
        placeholder="예: 개봉일 스크린수가 많을수록 총 관객도 많아지는 경향이 나타난다.",
        key="scatter_insight",
        label_visibility="collapsed",
    )


st.divider()


# ============================================================
# 5. 영화가 10편 이상인 장르의 총 관객 박스플롯
# ============================================================

st.header("5. 장르별 총 관객 분포 비교")

genre_movie_counts = df["genre"].value_counts()

# 영화가 10편 이상인 장르만 선택
selected_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index.tolist()

box_df = df[
    df["genre"].isin(selected_genres)
].dropna(
    subset=["genre", "total_audi", "movieNm"]
).copy()

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객",
    },
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{x}<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객",
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig5, use_container_width=True)

st.caption(
    "※ 영화가 10편 이상인 장르만 표시했습니다. "
    "상자 밖의 점은 해당 장르의 일반적인 범위에서 벗어난 값(이상치)입니다."
)

with st.container(border=True):
    st.subheader("이 그래프로 알 수 있는 것")
    st.text_input(
        "한 문장으로 정리해 보세요.",
        placeholder="예: ○○ 장르는 총 관객의 중앙값이 높고 영화별 관객 차이도 크게 나타난다.",
        key="boxplot_insight",
        label_visibility="collapsed",
    )


st.divider()


# ============================================================
# 6. 버블 산점도
# ============================================================

st.header("6. 개봉일 스크린수 × 총 관객 × 첫 주 관객")

bubble_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "genre",
    ]
).copy()

# Plotly의 버블 크기가 지나치게 작거나 큰 것을 방지하기 위한
# 최소 크기/최대 크기 설정
fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    size_max=45,
    hover_name="movieNm",
    title="첫 주 관객을 버블 크기로 나타낸 산점도",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "genre": "장르",
    },
)

fig6.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}<br>"
        "총 관객: %{y:,.0f}명<br>"
        "첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig6, use_container_width=True)

with st.container(border=True):
    st.subheader("이 그래프로 알 수 있는 것")
    st.text_input(
        "한 문장으로 정리해 보세요.",
        placeholder="예: 첫 주 관객이 많았던 영화일수록 큰 버블로 나타나며 총 관객과의 관계를 함께 볼 수 있다.",
        key="bubble_insight",
        label_visibility="collapsed",
    )


st.divider()


# ============================================================
# 7. 제작 국가 → 장르 선버스트
# ============================================================

st.header("7. 제작 국가에서 장르로 내려가는 분포")

sunburst_df = df[
    ["nation", "genre", "movieNm"]
].dropna(
    subset=["nation", "genre"]
).copy()

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    title="제작 국가 → 장르별 영화 편수",
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig7, use_container_width=True)

with st.container(border=True):
    st.subheader("이 그래프로 알 수 있는 것")
    st.text_input(
        "한 문장으로 정리해 보세요.",
        placeholder="예: 제작 국가별로 영화 수의 차이가 있으며, 국가 안에서도 장르 구성이 다르게 나타난다.",
        key="sunburst_insight",
        label_visibility="collapsed",
    )
