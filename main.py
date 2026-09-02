import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# 🎬 기본 설정
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.set_page_config(
    page_title="영화 데이터 그래프 도감 🎬",
    page_icon="🍿",
    layout="wide",
)

# ============================================================
# 🎀 귀여운 CSS
# ============================================================

st.markdown(
    """
    <style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(
            135deg,
            #fff7fb 0%,
            #f7f9ff 45%,
            #f2fbff 100%
        );
    }

    /* 메인 컨테이너 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    /* 제목 */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        color: #5b4b8a;
        margin-bottom: 0.3rem;
        text-shadow: 3px 3px 0px #ffd9ec;
    }

    .sub-title {
        text-align: center;
        font-size: 1.15rem;
        color: #777;
        margin-bottom: 2rem;
    }

    /* 섹션 제목 */
    .section-title {
        background: linear-gradient(
            90deg,
            #ffe5f0,
            #eee7ff,
            #e2f7ff
        );
        border-radius: 22px;
        padding: 14px 22px;
        margin-top: 1rem;
        margin-bottom: 1rem;
        color: #51466f;
        font-weight: 800;
        box-shadow: 0 5px 15px rgba(120, 100, 150, 0.08);
    }

    /* 설명 카드 */
    .insight-card {
        background: white;
        border: 2px solid #eee5f5;
        border-radius: 20px;
        padding: 18px 22px;
        margin: 12px 0 28px 0;
        box-shadow: 0 6px 18px rgba(100, 90, 130, 0.08);
    }

    .insight-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #725c9e;
        margin-bottom: 8px;
    }

    /* 작은 뱃지 */
    .badge {
        display: inline-block;
        padding: 6px 13px;
        border-radius: 999px;
        background: #fff0f7;
        color: #b45b87;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 3px;
    }

    /* 데이터 카드 */
    .stat-card {
        background: rgba(255,255,255,0.85);
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        border: 2px solid #eee8f5;
        box-shadow: 0 5px 15px rgba(100, 90, 130, 0.07);
    }

    .stat-number {
        font-size: 1.8rem;
        font-weight: 900;
        color: #65558f;
    }

    .stat-label {
        color: #888;
        font-size: 0.9rem;
    }

    /* Streamlit alert를 귀엽게 */
    div[data-testid="stAlert"] {
        border-radius: 18px;
        border: none;
    }

    /* 구분선 */
    hr {
        margin: 2.5rem 0;
        border: none;
        border-top: 2px dashed #e7dff0;
    }

    /* 입력창 */
    div[data-testid="stTextInput"] input {
        border-radius: 14px;
        border: 2px solid #eadff2;
        background: #fffafd;
    }

    /* Plotly 그래프 주변 */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255,255,255,0.7);
        border-radius: 22px;
        padding: 8px;
        box-shadow: 0 6px 20px rgba(100, 90, 130, 0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 📦 데이터 불러오기
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_URL,
        dtype={
            "movieCd": str,
            "openDt": str,
        },
    )

    # 장르가 여러 개라면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|", n=1)
        .str[0]
        .str.strip()
        .replace("", "미상")
    )

    # 제작 국가
    df["nation"] = (
        df["nation"]
        .fillna("미상")
        .astype(str)
        .str.strip()
        .replace("", "미상")
    )

    return df


try:
    df = load_data()
except Exception as e:
    st.error("앗! 😭 데이터를 불러오지 못했어요.")
    st.exception(e)
    st.stop()


# 숫자형 데이터
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
# 🍿 메인 타이틀
# ============================================================

st.markdown(
    '<div class="main-title">🎬 영화 데이터 그래프 도감 2 🍿</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-title">✨ 분포와 관계를 귀엽게 살펴보는 영화 데이터 탐험 ✨</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="text-align:center;">
        <span class="badge">🎞️ 영화 216편</span>
        <span class="badge">🍿 박스오피스 TOP 10</span>
        <span class="badge">📊 데이터 시각화</span>
        <span class="badge">💫 Plotly</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ============================================================
# 📊 간단한 데이터 요약
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">🎬 {len(df)}편</div>
            <div class="stat-label">분석한 영화</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">🎨 {df["genre"].nunique()}개</div>
            <div class="stat-label">장르</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">🌏 {df["nation"].nunique()}개</div>
            <div class="stat-label">제작 국가</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")
st.divider()


# ============================================================
# 📝 그래프 아래 공통 문구 영역
# ============================================================

def insight_box(key, placeholder):
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">
                💡 이 그래프로 알 수 있는 것
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_input(
        "한 문장으로 정리해 보세요 ✍️",
        placeholder=placeholder,
        key=key,
        label_visibility="collapsed",
    )


# ============================================================
# 1️⃣ 장르별 영화 편수
# ============================================================

st.markdown(
    '<div class="section-title">1️⃣ 🎨 장르별 영화 편수</div>',
    unsafe_allow_html=True,
)

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
    hole=0.52,
    title="🍩 어떤 장르의 영화가 가장 많을까?",
)

fig1.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "🎬 <b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    ),
)

fig1.update_layout(
    legend_title_text="🎨 장르",
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig1, use_container_width=True)

insight_box(
    "genre_insight",
    "예: 가장 많은 장르는 ○○이고 전체 영화의 약 ○○%를 차지한다.",
)

st.divider()


# ============================================================
# 2️⃣ 장르 → 영화 트리맵
# ============================================================

st.markdown(
    '<div class="section-title">2️⃣ 🌳 장르 속 영화 트리맵</div>',
    unsafe_allow_html=True,
)

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].dropna(
    subset=["movieNm", "total_audi"]
)

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="🌳 칸이 클수록 총 관객이 많은 영화!",
)

fig2.update_traces(
    hovertemplate=(
        "🎬 <b>%{label}</b><br>"
        "🍿 총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig2, use_container_width=True)

st.caption("👀 영화 칸에 마우스를 살짝 올려 보세요!")

insight_box(
    "treemap_insight",
    "예: ○○ 장르에서 총 관객이 많은 영화들이 특히 크게 나타난다.",
)

st.divider()


# ============================================================
# 3️⃣ 총 관객 히스토그램
# ============================================================

st.markdown(
    '<div class="section-title">3️⃣ 🍿 총 관객은 어디에 몰려 있을까?</div>',
    unsafe_allow_html=True,
)

hist_df = df.dropna(subset=["total_audi"]).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="📊 영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객",
        "count": "영화 편수",
    },
)

fig3.update_traces(
    hovertemplate=(
        "🍿 총 관객 구간: %{x}<br>"
        "🎬 영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="🍿 총 관객",
    yaxis_title="🎬 영화 편수",
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig3, use_container_width=True)


# 가장 관객이 많은 영화
max_audience_row = df.loc[df["total_audi"].idxmax()]
max_movie = max_audience_row["movieNm"]
max_audience = max_audience_row["total_audi"]

# 가장 영화가 많이 몰린 구간
counts, bin_edges = pd.cut(
    hist_df["total_audi"],
    bins=20,
    retbins=True,
    include_lowest=True,
)

bin_counts = counts.value_counts().sort_index()
most_common_bin = bin_counts.idxmax()

st.success(
    f"🎯 **영화가 가장 많이 몰려 있는 구간:** "
    f"{most_common_bin.left:,.0f}명 ~ {most_common_bin.right:,.0f}명  \n"
    f"🏆 **가장 많은 관객을 모은 영화:** "
    f"**{max_movie}** — {max_audience:,.0f}명"
)

insight_box(
    "histogram_insight",
    "예: 대부분의 영화는 ○○만 명 이하 구간에 몰려 있으며, 가장 많은 관객을 모은 영화는 ○○이다.",
)

st.divider()


# ============================================================
# 4️⃣ 스크린수 × 총 관객 산점도
# ============================================================

st.markdown(
    '<div class="section-title">4️⃣ 🔍 개봉일 스크린수와 총 관객의 관계</div>',
    unsafe_allow_html=True,
)

scatter_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "movieNm",
        "genre",
    ]
).copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="🔎 스크린수가 많으면 관객도 많을까?",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "genre": "장르",
    },
)

fig4.update_traces(
    hovertemplate=(
        "🎬 <b>%{hovertext}</b><br>"
        "📺 개봉일 스크린수: %{x:,.0f}<br>"
        "🍿 총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig4, use_container_width=True)

st.caption("🖱️ 점에 마우스를 올리면 영화 이름을 확인할 수 있어요!")

insight_box(
    "scatter_insight",
    "예: 개봉일 스크린수가 많을수록 총 관객도 많아지는 경향이 나타난다.",
)

st.divider()


# ============================================================
# 5️⃣ 장르별 박스플롯
# ============================================================

st.markdown(
    '<div class="section-title">5️⃣ 📦 장르별 총 관객 박스플롯</div>',
    unsafe_allow_html=True,
)

genre_movie_counts = df["genre"].value_counts()

selected_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index.tolist()

box_df = df[
    df["genre"].isin(selected_genres)
].dropna(
    subset=[
        "genre",
        "total_audi",
        "movieNm",
    ]
).copy()

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_name="movieNm",
    title="📦 영화가 10편 이상인 장르만 비교!",
    labels={
        "genre": "장르",
        "total_audi": "총 관객",
    },
)

fig5.update_traces(
    hovertemplate=(
        "🎬 <b>%{hovertext}</b><br>"
        "🎨 장르: %{x}<br>"
        "🍿 총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="🎨 장르",
    yaxis_title="🍿 총 관객",
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig5, use_container_width=True)

st.caption(
    "📦 상자 밖으로 톡 튀어나온 점은 해당 장르에서 상대적으로 특이한 관객 수를 가진 영화예요!"
)

insight_box(
    "boxplot_insight",
    "예: ○○ 장르는 총 관객의 중앙값이 높고 영화별 관객 차이도 크게 나타난다.",
)

st.divider()


# ============================================================
# 6️⃣ 버블 산점도
# ============================================================

st.markdown(
    '<div class="section-title">6️⃣ 🫧 첫 주 관객 버블 산점도</div>',
    unsafe_allow_html=True,
)

bubble_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "genre",
    ]
).copy()

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    size_max=45,
    hover_name="movieNm",
    title="🫧 버블이 클수록 첫 주 관객이 많아요!",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "genre": "장르",
    },
)

fig6.update_traces(
    hovertemplate=(
        "🎬 <b>%{hovertext}</b><br>"
        "📺 개봉일 스크린수: %{x:,.0f}<br>"
        "🍿 총 관객: %{y:,.0f}명<br>"
        "🚀 첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig6, use_container_width=True)

st.caption(
    "🫧 같은 산점도인데 이번에는 첫 주 관객을 버블 크기로 표현했어요!"
)

insight_box(
    "bubble_insight",
    "예: 첫 주 관객이 많았던 영화일수록 큰 버블로 나타나며 총 관객과의 관계를 함께 볼 수 있다.",
)

st.divider()


# ============================================================
# 7️⃣ 제작 국가 → 장르 선버스트
# ============================================================

st.markdown(
    '<div class="section-title">7️⃣ 🌞 제작 국가 → 장르 선버스트</div>',
    unsafe_allow_html=True,
)

sunburst_df = df[
    ["nation", "genre"]
].dropna(
    subset=[
        "nation",
        "genre",
    ]
).copy()

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    title="🌏 어느 나라에서 어떤 장르의 영화를 만들었을까?",
)

fig7.update_traces(
    hovertemplate=(
        "🎬 <b>%{label}</b><br>"
        "📚 영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    margin=dict(t=70, l=20, r=20, b=20),
)

st.plotly_chart(fig7, use_container_width=True)

st.caption(
    "🌞 바깥쪽으로 갈수록 장르예요! 국가 → 장르 순서로 내려가며 살펴볼 수 있어요."
)

insight_box(
    "sunburst_insight",
    "예: 제작 국가별로 영화 수의 차이가 있으며 국가 안에서도 장르 구성이 다르게 나타난다.",
)


# ============================================================
# 🎉 마무리
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:25px;
        border-radius:25px;
        background:linear-gradient(135deg,#fff0f7,#f1edff,#e8f9ff);
    ">
        <div style="font-size:2rem;">🎬 🍿 🎨 📊 🫧 🌳 🌞</div>
        <h3 style="color:#65558f;">영화 데이터 탐험 완료! 🎉</h3>
        <p style="color:#777;">
            그래프를 이리저리 움직여 보고 👀<br>
            마우스를 올려 영화 정보를 찾아보세요! 🔎✨
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
