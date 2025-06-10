import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(layout="wide")

st.title("글로벌 시가총액 Top 10 기업 주가 변화 (최근 3년)")
st.markdown("""
이 앱은 글로벌 시가총액 상위 기업들의 지난 3년간 주가 변화를 시각화합니다.
Plotly를 사용하여 인터랙티브한 차트를 제공합니다.
""")

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

end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365)

@st.cache_data
def get_stock_data(tickers, start, end):
    data = {}
    for name, ticker in tickers.items():
        try:
            df = yf.download(ticker, start=start, end=end, auto_adjust=False)
            if not df.empty:
                if 'Adj Close' in df.columns:
                    data[name] = df['Adj Close']
                elif 'Close' in df.columns:
                    st.warning(f"{name} ({ticker}) 의 'Adj Close' 없음. 'Close' 사용.")
                    data[name] = df['Close']
                else:
                    st.warning(f"{name} ({ticker}) 데이터에 유효한 종가 없음.")
            else:
                st.warning(f"{name} ({ticker}) 의 데이터를 가져올 수 없습니다.")
        except Exception as e:
            st.error(f"{name} ({ticker}) 데이터 오류: {e}")

    if not data:
        st.error("오류: 모든 기업의 주가 데이터를 가져오는 데 실패했습니다.")
        return pd.DataFrame()

    try:
        df = pd.concat(data.values(), axis=1, join='inner')
        df.columns = list(data.keys())

        if df.isnull().all().all():
            st.error("오류: 모든 값이 NaN입니다.")
            return pd.DataFrame()

        return df
    except Exception as e:
        st.error(f"오류: 주가 데이터로 DataFrame을 생성하는 데 문제가 발생했습니다. {e}")
        return pd.DataFrame()

with st.spinner("주가 데이터를 불러오는 중..."):
    df_stocks = get_stock_data(TICKERS, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

if not df_stocks.empty:
    st.write(f"**데이터 기간:** {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
    available_companies = [col for col in df_stocks.columns if not df_stocks[col].isnull().all()]

    selected_companies = st.multiselect(
        "**시각화할 기업을 선택하세요:**",
        options=list(TICKERS.keys()),
        default=available_companies
    )

    if selected_companies:
        final_selected = [comp for comp in selected_companies if comp in available_companies]
        df_selected = df_stocks[final_selected]

        # 정규화된 주가
        st.subheader("📊 주가 변화율 (첫 날짜 기준 정규화)")
        base = df_selected.iloc[0].replace({0: 1}).fillna(1)
        normalized_df = df_selected.divide(base)

        if not normalized_df.empty:
            normalized_melt = normalized_df.reset_index().melt(id_vars='Date', var_name='기업', value_name='정규화 주가') \
                if 'Date' in normalized_df.columns else normalized_df.reset_index().melt(id_vars='index', var_name='기업', value_name='정규화 주가')
            normalized_melt.rename(columns={"index": "날짜"}, inplace=True)

            fig_norm = px.line(
                normalized_melt,
                x="날짜",
                y="정규화 주가",
                color="기업",
                template="plotly_white",
                title="정규화된 주가 변화율"
            )
            fig_norm.update_layout(hovermode="x unified")
            st.plotly_chart(fig_norm, use_container_width=True)
        else:
            st.warning("정규화된 데이터를 표시할 수 없습니다.")

        st.markdown("---")

        # 실제 주가
        st.subheader("💰 실제 주가 (USD)")
        actual_melt = df_selected.reset_index().melt(id_vars='Date', var_name='기업', value_name='주가') \
            if 'Date' in df_selected.columns else df_selected.reset_index().melt(id_vars='index', var_name='기업', value_name='주가')
        actual_melt.rename(columns={"index": "날짜"}, inplace=True)

        fig_actual = px.line(
            actual_melt,
            x="날짜",
            y="주가",
            color="기업",
            template="plotly_white",
            title="실제 주가 추이"
        )
        fig_actual.update_layout(hovermode="x unified")
        st.plotly_chart(fig_actual, use_container_width=True)

        st.markdown("---")

        st.subheader("📋 데이터 미리보기")
        st.dataframe(df_selected.tail())

    else:
        st.info("시각화할 기업을 선택해주세요.")
else:
    st.error("주가 데이터를 불러오는 데 실패했습니다. `yfinance` 서버 상태 또는 종목 코드 확인이 필요합니다.")

st.markdown("""
---
**참고:**
- 시가총액 상위 10개 기업 리스트는 실시간으로 변동될 수 있습니다.
- 주가 데이터는 `yfinance`에서 제공되며 종가(Adj Close)를 기준으로 합니다.
""")
