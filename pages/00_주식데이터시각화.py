import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title('📈 주식 시세 시각화')
ticker = st.text_input('종목 코드 입력 (예: AAPL, 005930.KS)', 'AAPL')

data = yf.download(ticker, start='2023-01-01')
st.write(f'{ticker} 주식 데이터')
st.dataframe(data.tail())

fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='종가'))
fig.update_layout(title=f'{ticker} 주가 추이', xaxis_title='날짜', yaxis_title='가격')
st.plotly_chart(fig)
