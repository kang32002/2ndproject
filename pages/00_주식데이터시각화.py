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
            df = yf.download(ticker, start=start, end=end, auto_adjust=False)
            if not df.empty and 'Adj Close' in df.columns:
                data[name] = df['Adj Close']
            elif not df.empty and 'Close' in df.columns:
                st.warning(f"경고: {name} ({ticker}) 의 'Adj Close' 데이터를 찾을 수 없어 'Close' 데이터를 사용합니다.")
                data[name] = df['Close']
            else:
                st.warning(f"경고: {name} ({ticker}) 의 주가 데이터를 가져오지 못했습니다. 이 기업은 시각화에서 제외됩니다.")
        except Exception as e:
            st.error(f"오류: {name} ({ticker}) 의 데이터를 가져오는 중 오류 발생: {e}. 이 기업은 시각화에서 제외됩니다.")

    # --- 핵심 수정 부분 ---
    # data 딕셔너리가 비어있는지 확인
    if not data:
        st.error("오류: 모든 기업의 주가 데이터를 가져오는 데 실패했습니다. DataFrame을 생성할 수 없습니다.")
        return pd.DataFrame() # 빈 DataFrame 반환하여 오류 회피

    # 데이터의 인덱스를 일치시키기 위한 재정렬
    # Series들이 동일한 인덱스를 가지지 않으면 NaN이 발생할 수 있으므로,
    # 모든 Series를 공통 인덱스(union)에 맞춰 재인덱싱합니다.
    # 이 부분은 현재 오류와 직접 관련 없지만, 데이터 프레임 안정성 향상에 도움이 됩니다.
    # 모든 Series가 비어있다면 이 단계에서도 문제가 발생할 수 있으므로, 위의 `if not data:`가 더 중요합니다.
    try:
        # 모든 Series의 인덱스를 합집합으로 만들고, 해당 인덱스에 맞춰 재구성합니다.
        # 이렇게 하면 Pandas가 DataFrame을 만들 때 모든 Series의 인덱스가 동일하다고 판단하여 오류를 피할 수 있습니다.
        # 하지만, `pd.DataFrame(data)`가 직접 던지는 ValueError는 Series가 모두 비어있을 때 발생합니다.
        # 따라서, 이 부분은 데이터가 있긴 하지만 인덱스가 다를 경우에 대비하는 것이고,
        # 핵심은 `data` 딕셔너리에 유효한 Series가 하나라도 포함되어 있는지 확인하는 것입니다.
        # 여기서는 단순히 `pd.DataFrame(data)`를 시도하고 실패하면 빈 DataFrame을 반환하는 방식으로 충분합니다.
        
        # DataFrame 생성 시 모든 Series의 인덱스가 자동으로 맞춰지므로, 이 복잡한 재인덱싱은 필요 없을 수 있습니다.
        # 문제는 data 딕셔너리가 완전히 비어있거나, 모든 Series가 비어있을 때입니다.
        df_result = pd.DataFrame(data)
        # 모든 컬럼이 NaN인 경우 (모든 데이터 로딩 실패)
        if df_result.isnull().all().all():
             st.error("오류: 데이터를 가져왔지만 모든 값이 NaN입니다. 유효한 주가 데이터를 찾을 수 없습니다.")
             return pd.DataFrame() # 빈 DataFrame 반환
        return df_result

    except ValueError as ve:
        st.error(f"오류: 주가 데이터로 DataFrame을 생성하는 데 문제가 발생했습니다. {ve}")
        st.error("모든 기업의 데이터를 가져오는 데 실패했거나, 가져온 데이터가 유효하지 않을 수 있습니다.")
        return pd.DataFrame() # 빈 DataFrame 반환

# 데이터 가져오기
with st.spinner("주가 데이터를 불러오는 중... 잠시만 기다려 주세요."):
    df_stocks = get_stock_data(TICKERS, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

if not df_stocks.empty: # 빈 DataFrame이 아닐 때만 다음 로직 실행
    st.write(f"**데이터 기간:** {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

    # df_stocks.columns는 실제로 데이터를 성공적으로 가져온 기업의 이름만 포함해야 함
    available_companies = [col for col in df_stocks.columns if not df_stocks[col].isnull().all()] # 모든 값이 NaN인 컬럼은 제외
    
    # 기본 선택을 실제 데이터가 있는 기업으로 설정
    default_selection = available_companies
    selected_companies = st.multiselect(
        "**시각화할 기업을 선택하세요:**",
        options=list(TICKERS.keys()), # 모든 기업을 옵션으로 보여주지만
        default=default_selection      # 실제로 데이터가 있는 기업만 기본 선택
    )

    if selected_companies:
        # 선택된 기업 중 실제로 데이터가 있는 기업만 필터링
        final_selected_companies = [comp for comp in selected_companies if comp in available_companies]
        
        if not final_selected_companies:
            st.warning("선택하신 기업 중 유효한 주가 데이터가 있는 기업이 없습니다. 다른 기업을 선택해주세요.")
            st.stop() # 더 이상 진행하지 않고 중단
            
        df_selected = df_stocks[final_selected_companies]

        # --- 주가 변화율 시각화 (첫 날짜 기준 정규화) ---
        st.subheader("📊 주가 변화율 (첫 날짜 기준 정규화)")
        # 첫 날의 값을 1로 설정하여 정규화. 첫 날 데이터가 NaN인 경우를 대비
        normalized_df = df_selected / df_selected.iloc[0].replace(0, 1) # 0으로 나누는 오류 방지
        # 첫 날 값이 NaN인 컬럼은 정규화에서 제외하거나 적절히 처리해야 함
        normalized_df = normalized_df.dropna(axis=1, how='all') # 모든 값이 NaN인 컬럼 제거

        if not normalized_df.empty:
            fig_normalized = px.line(
                normalized_df,
                x=normalized_df.index,
                y=normalized_df.columns,
                title='첫 날짜 기준 주가 변화율',
                labels={'value': '정규화된 주가', 'index': '날짜'},
                hover_name=normalized_df.columns,
                template="plotly_white"
            )
            fig_normalized.update_layout(hovermode="x unified")
            st.plotly_chart(fig_normalized, use_container_width=True)
            st.caption("첫 날짜를 기준으로 주가 변화율을 정규화하여 비교합니다. 1은 첫 날의 주가입니다.")
        else:
            st.warning("정규화된 주가 데이터를 생성할 수 없습니다.")
        st.markdown("---")

        # --- 실제 주가 시각화 (USD) ---
        st.subheader("💰 실제 주가 (USD)")
        if not df_selected.empty:
            fig_actual = px.line(
                df_selected,
                x=df_selected.index,
                y=df_selected.columns,
                title='실제 주가 추이',
                labels={'value': '주가 (USD)', 'index': '날짜'},
                hover_name=df_selected.columns,
                template="plotly_white"
            )
            fig_actual.update_layout(hovermode="x unified")
            st.plotly_chart(fig_actual, use_container_width=True)
            st.caption("선택된 기업들의 실제 주가입니다.")
        else:
            st.warning("실제 주가 데이터를 시각화할 수 없습니다.")
        st.markdown("---")

        st.subheader("📋 데이터 미리보기")
        if not df_selected.empty:
            st.dataframe(df_selected.tail())
        else:
            st.info("표시할 데이터가 없습니다.")

    else:
        st.info("시각화할 기업을 한 개 이상 선택해주세요.")
else:
    st.error("**주가 데이터를 불러오는 데 실패했습니다.** 앱을 다시 시도하거나, `yfinance` 서버의 일시적인 문제일 수 있습니다. 로그를 확인하여 상세 오류를 파악해주세요.")

st.markdown("""
---
**참고:**
- 시가총액 상위 10개 기업 리스트는 실시간으로 변동될 수 있습니다. 본 앱에서는 `yfinance`에서 접근 가능한 주요 기업들을 선정했습니다.
- 주가 데이터는 `yfinance`에서 제공되며, 종가(Adj Close)를 기준으로 합니다.
- 데이터 로딩 시간은 네트워크 상황 및 `yfinance` 서버 응답에 따라 달라질 수 있습니다.
""")
