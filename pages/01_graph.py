import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

st.title("일차방정식 $y = mx + n$ 그래프 시각화")
st.write("Plotly를 이용하여 입력받은 기울기($m$)와 y절편($n$) 값에 해당하는 직선을 좌표평면에 표시합니다.")

# 사용자로부터 m과 n 값 입력받기
col1, col2 = st.columns(2)
with col1:
    m = st.number_input("기울기 (m)를 입력하세요:", value=1.0, format="%.2f")
with col2:
    n = st.number_input("y절편 (n)을 입력하세요:", value=0.0, format="%.2f")

st.markdown(f"입력된 값: $y = {m}x + {n}$")

# x 값 범위 설정 (그래프의 가로축 범위)
x = np.linspace(-10, 10, 400) # -10부터 10까지 400개의 점 생성
y = m * x + n

# Plotly 그래프 생성
fig = go.Figure()

# 일차방정식 그래프 추가
fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name=f'$y = {m}x + {n}$',
        line=dict(color='blue', width=3)
    )
)

# 그래프 레이아웃 설정
fig.update_layout(
    title=f"직선 $y = {m}x + {n}$",
    xaxis_title="x",
    yaxis_title="y",
    xaxis=dict(
        showgrid=True,
        zeroline=True,
        zerolinecolor='lightgray',
        gridcolor='lightgray',
        range=[-10, 10] # x축 범위 설정
    ),
    yaxis=dict(
        showgrid=True,
        zeroline=True,
        zerolinecolor='lightgray',
        gridcolor='lightgray',
        range=[-10, 10] # y축 범위 설정 (자동 조절 대신 고정)
    ),
    height=600
)

# 스트림릿에 그래프 표시
st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.write("### 설명")
st.write(f"- 파란색 선은 입력된 기울기($m$)와 y절편($n$)에 따른 일차방정식 $y = {m}x + {n}$의 그래프입니다.")
st.write("- x축과 y축은 각각 -10부터 10까지의 범위를 가집니다.")
st.write("- **기울기($m$)**는 직선의 기울어진 정도를 나타내며, 양수이면 오른쪽 위로, 음수이면 오른쪽 아래로 향합니다.")
st.write("- **y절편($n$)**은 직선이 y축과 만나는 점의 y좌표를 나타냅니다.")
