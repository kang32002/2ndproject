import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide") # 페이지 레이아웃을 넓게 설정

st.title("글로벌 시가총액 Top 10 기업 주가 변화 (최근 3년)")

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
                st.warning(f"경고: {name} ({ticker}) 의 주가 데이터를 가져오지 못했습니다.")
        except Exception as e:
            st.error(f"오류: {name} ({ticker}) 의 데이터를 가져오는 중 오류 발생: {e}")
    return pd.DataFrame(data)

# 데이터 가져오기
with st.spinner("주가 데이터를 불러오는 중..."):
    df_stocks = get_stock_data(TICKERS, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

if not df_stocks.empty:
    st.write(f"데이터 기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

    # 모든 기업을 기본 선택으로 설정
    default_selection = list(TICKERS.keys())
    selected_companies = st.multiselect(
        "시각화할 기업을 선택하세요:",
        options=list(TICKERS.keys()),
        default=default_selection
    )

    if selected_companies:
        # 선택된 기업의 데이터만 필터링
        df_selected = df_stocks[selected_companies]

        # 모든 주가를 첫 날짜 기준으로 정규화하여 변화율 비교
        st.subheader("주가 변화율 (첫 날짜 기준 정규화)")
        # 첫 날의 값을 1로 설정하여 정규화
        normalized_df = df_selected / df_selected.iloc[0]
        st.line_chart(normalized_df)
        st.caption("첫 날짜를 기준으로 주가 변화율을 정규화하여 비교합니다. 1은 첫 날의 주가입니다.")

        st.subheader("실제 주가 (USD)")
        st.line_chart(df_selected)
        st.caption("선택된 기업들의 실제 주가입니다.")

        st.subheader("데이터 미리보기")
        st.dataframe(df_selected.tail()) # 최신 데이터 몇 개만 보여줌

    else:
        st.info("시각화할 기업을 한 개 이상 선택해주세요.")
else:
    st.error("주가 데이터를 불러오는 데 실패했습니다. 나중에 다시 시도해주세요.")

st.markdown("""
---
**참고:**
- 시가총액 상위 10개 기업 리스트는 실시간으로 변동될 수 있습니다. 본 앱에서는 yfinance에서 접근 가능한 주요 기업들을 선정했습니다.
- 주가 데이터는 `yfinance`에서 제공되며, 종가(Adj Close)를 기준으로 합니다.
- 데이터 로딩 시간은 네트워크 상황 및 yfinance 서버 응답에 따라 달라질 수 있습니다.
""")
