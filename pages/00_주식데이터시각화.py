import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide") # 페이지 레이아웃을 넓게 설정

st.title("글로벌 시가총액 Top 10 기업 주가 변화 (최근 3년)")
st.markdown("""
이 앱은 글로벌 시가총액 상위 기업들의 지난 3년간 주가 변화를 시각화합니다.
Plotly를 사용하여 인터랙티브한 차트를 제공합니다.
""")

# 글로벌 시가총액 상위 10개 기업 (yfinance 접근성 고려)
# 실제 시총 순위는 변동되므로 참고용 리스트입니다.
TICKERS = {
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "NVIDIA": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Meta Platforms": "META",
    "Berkshire Hathaway": "BRK-B",
    "Eli Lilly": "LLY",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

# 최근 3년 날짜 범위 설정
end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365) # 대략 3년

@st.cache_data # 데이터 캐싱으로 성능 향상
def get_stock_data(tickers, start, end):
    data = {}
    for name, ticker in tickers.items():
        try:
            # 주가 데이터 가져오기 (종가 기준)
            df = yf.download(ticker, start=start, end=end)
            if not df.empty:
                data[name] = df['Adj Close']
            else:
                st.warning(f"경고: {name} ({ticker}) 의 주가 데이터를 가져오지 못했습니다. 이 기업은 시각화에서 제외됩니다.")
        except Exception as e:
            st.error(f"오류: {name} ({ticker}) 의 데이터를 가져오는 중 오류 발생: {e}. 이 기업은 시각화에서 제외됩니다.")
    return pd.DataFrame(data)

# 데이터 가져오기
with st.spinner("주가 데이터를 불러오는 중... 잠시만 기다려 주세요."):
    df_stocks = get_stock_data(TICKERS, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

if not df_stocks.empty:
    st.write(f"**데이터 기간:** {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

    # 모든 기업을 기본 선택으로 설정
    default_selection = [company for company in TICKERS.keys() if company in df_stocks.columns]
    selected_companies = st.multiselect(
        "**시각화할 기업을 선택하세요:**",
        options=list(TICKERS.keys()),
        default=default_selection
    )

    if selected_companies:
        # 선택된 기업의 데이터만 필터링
        df_selected = df_stocks[selected_companies]

        # --- 주가 변화율 시각화 (첫 날짜 기준 정규화) ---
        st.subheader("📊 주가 변화율 (첫 날짜 기준 정규화)")
        # 첫 날의 값을 1로 설정하여 정규화
        normalized_df = df_selected / df_selected.iloc[0]

        # Plotly Express를 사용하여 선 차트 생성
        fig_normalized = px.line(
            normalized_df,
            x=normalized_df.index,
            y=normalized_df.columns,
            title='첫 날짜 기준 주가 변화율',
            labels={'value': '정규화된 주가', 'index': '날짜'},
            hover_name=normalized_df.columns,
            template="plotly_white" # 깔끔한 템플릿 사용
        )
        fig_normalized.update_layout(hovermode="x unified") # 통합 호버 모드
        st.plotly_chart(fig_normalized, use_container_width=True)
        st.caption("첫 날짜를 기준으로 주가 변화율을 정규화하여 비교합니다. 1은 첫 날의 주가입니다.")
        st.markdown("---")

        # --- 실제 주가 시각화 (USD) ---
        st.subheader("💰 실제 주가 (USD)")
        # Plotly Express를 사용하여 선 차트 생성
        fig_actual = px.line(
            df_selected,
            x=df_selected.index,
            y=df_selected.columns,
            title='실제 주가 추이',
            labels={'value': '주가 (USD)', 'index': '날짜'},
            hover_name=df_selected.columns,
            template="plotly_white" # 깔끔한 템플릿 사용
        )
        fig_actual.update_layout(hovermode="x unified") # 통합 호버 모드
        st.plotly_chart(fig_actual, use_container_width=True)
        st.caption("선택된 기업들의 실제 주가입니다.")
        st.markdown("---")

        st.subheader("📋 데이터 미리보기")
        st.dataframe(df_selected.tail()) # 최신 데이터 몇 개만 보여줌

    else:
        st.info("시각화할 기업을 한 개 이상 선택해주세요.")
else:
    st.error("주가 데이터를 불러오는 데 실패했습니다. 나중에 다시 시도해주세요. (팁: yfinance의 일시적인 문제일 수 있습니다.)")

st.markdown("""
---
**참고:**
- 시가총액 상위 10개 기업 리스트는 실시간으로 변동될 수 있습니다. 본 앱에서는 `yfinance`에서 접근 가능한 주요 기업들을 선정했습니다.
- 주가 데이터는 `yfinance`에서 제공되며, 종가(Adj Close)를 기준으로 합니다.
- 데이터 로딩 시간은 네트워크 상황 및 `yfinance` 서버 응답에 따라 달라질 수 있습니다.
""")
