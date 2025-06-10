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
            if not df.empty and 'Adj Close' in df.columns:
                data[name] = df['Adj Close']
            elif not df.empty and 'Close' in df.columns:
                st.warning(f"{name} ({ticker})는 'Adj Close'가 없어 'Close'를 사용합니다.")
                data[name] = df['Close']
            else:
                st.warning(f"{name} ({ticker})의 주가 데이터를 가져오지 못했습니다.")
        except Exception as e:
            st.error(f"{name} ({ticker}) 데이터를 가져오는 중 오류 발생: {e}")

    if not data:
        st.error("모든 기업의 데이터를 가져오는 데 실패했습니다.")
        return pd.DataFrame()

    try:
        df_result = pd.DataFrame(data)
        if df_result.isnull().all().all():
            st.error("데이터는 있지만 모든 값이 NaN입니다.")
            return pd.DataFrame()
        return df_result
    except ValueError as ve:
        st.error(f"DataFrame 생성 오류: {ve}")
        return pd.DataFrame()

with st.spinner("주가 데이터를 불러오는 중입니다..."):
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
        final_selected_companies = [comp for comp in selected_companies if comp in available_companies]
        if not final_selected_companies:
            st.warning("선택한 기업 중 데이터가 있는 항목이 없습니다.")
            st.stop()

        df_selected = df_stocks[final_selected_companies]

        # 🔧 인덱스 이름 지정
        df_selected = df_selected.copy()
        df_selected.index.name = "날짜"

        # 🔄 정규화
        st.subheader("📊 주가 변화율 (정규화)")
        normalized_df = df_selected / df_selected.iloc[0].replace(0, 1)
        normalized_df = normalized_df.dropna(axis=1, how='all')
        normalized_df.index.name = "날짜"
        normalized_melt = normalized_df.reset_index().melt(id_vars="날짜", var_name="기업", value_name="정규화 주가")

        if not normalized_melt.empty:
            fig_normalized = px.line(
                normalized_melt,
                x="날짜", y="정규화 주가", color="기업",
                title="정규화된 주가 변화율",
                template="plotly_white"
            )
            fig_normalized.update_layout(hovermode="x unified")
            st.plotly_chart(fig_normalized, use_container_width=True)
            st.caption("첫 날짜를 기준으로 1로 정규화된 주가 비교입니다.")
        else:
            st.warning("정규화된 데이터를 시각화할 수 없습니다.")

        st.markdown("---")

        # 📈 실제 주가 시각화
        st.subheader("💰 실제 주가 (USD)")
        actual_melt = df_selected.reset_index().melt(id_vars="날짜", var_name="기업", value_name="주가")

        if not actual_melt.empty:
            fig_actual = px.line(
                actual_melt,
                x="날짜", y="주가", color="기업",
                title="실제 주가 변화",
                template="plotly_white"
            )
            fig_actual.update_layout(hovermode="x unified")
            st.plotly_chart(fig_actual, use_container_width=True)
            st.caption("미국 달러 기준 실제 주가입니다.")
        else:
            st.warning("실제 주가 데이터를 시각화할 수 없습니다.")

        st.markdown("---")
        st.subheader("📋 데이터 미리보기")
        st.dataframe(df_selected.tail())

    else:
        st.info("시각화할 기업을 선택하세요.")

else:
    st.error("주가 데이터를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.")

st.markdown("""
---
**참고:**
- 시가총액 상위 기업 리스트는 참고용이며 변동될 수 있습니다.
- `yfinance`의 `Adj Close` 데이터를 기반으로 합니다.
- 데이터 로딩에는 시간이 걸릴 수 있습니다.
""")
