import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

st.title("일차방정식 <span class="math-inline">ax \+ by \+ c \= 0</span> 그래프 시각화")
st.write("Plotly를 이용하여 입력받은 <span class="math-inline">a</span>, <span class="math-inline">b</span>, <span class="math-inline">c</span> 값에 해당하는 직선을 좌표평면에 표시합니다.")

# 사용자로부터 a, b, c 값 입력받기
col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input("a 값을 입력하세요:", value=1.0, format="%.2f")
with col2:
    b = st.number_input("b 값을 입력하세요:", value=-1.0, format="%.2f")
with col3:
    c = st.number_input("c 값을 입력하세요:", value=0.0, format="%.2f")

st.markdown(f"입력된 방정식: <span class="math-inline">\{a\}x \+ \{b\}y \+ \{c\} \= 0</span>")

# 그래프 그리기 위한 x, y 값 계산
x = np.linspace(-10, 10, 400) # -10부터 10까지 400개의 점 생성

fig = go.Figure()

# Plotly 그래프 생성
if b == 0:
    if a != 0:
        # a != 0, b = 0 이면 ax + c = 0 => x = -c/a (수직선)
        x_val = -c / a
        fig.add_trace(
            go.Scatter(
                x=[x_val, x_val],
                y=[-10, 10], # y축 범위에 맞게 설정
                mode='lines',
                name=f'<span class="math-inline">x \= \{\-c/a\}</span>',
                line=dict(color='red', width=4) # 수직선은 붉은색, 더 굵게
            )
        )
        st.info(f"이는 수직선 <span class="math-inline">x \= \{\-c/a\}</span> 입니다.")
    else:
        # a = 0, b = 0 인 경우
        if c == 0:
            st.warning("방정식 <span class="math-inline">0x \+ 0y \+ 0 \= 0</span>은 모든 실수 x, y에 대해 성립하므로, **좌표평면 전체**를 나타냅니다.")
        else:
            st.error(f"방정식 <span class="math-inline">0x \+ 0y \+ \{c\} \= 0</span> (즉, <span class="math-inline">\{c\} \= 0</span>)은 성립하지 않으므로, **그래프가 존재하지 않습니다.**")
        st.plotly_chart(fig, use_container_width=True) # 빈 그래프라도 표시
        st.stop() # 더 이상 코드 실행하지 않음
else:
    # b != 0 이므로, y = (-a/b)x - (c/b) (일반적인 기울기를 가진 직선)
    y = (-a / b) * x - (c / b)

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name=f'<span class="math-inline">\{a\}x \+ \{b\}y \+ \{c\} \= 0</span>',
            line=dict(color='blue', width=3)
        )
    )
    if a == 0:
        # a = 0, b != 0 이면 by + c = 0 => y = -c/b (수평선)
        st.info(f"이는 수평선 <span class="math-inline">y \= \{\-c/b\}</span> 입니다.")


# 그래프 레이아웃 설정
fig.update_layout(
    title=f"직선 <span class="math-inline">\{a\}x \+ \{b\}y \+ \{c\} \= 0</span>",
    xaxis_title="x",
    yaxis_title="y",
    xaxis=dict(
        showgrid=True,
        zeroline=True,
        zerolinecolor='black', # 0점 선을 더 뚜렷하게
        zerolinewidth=2,       # 0점 선 두께
        gridcolor='lightgray',
        griddash='dot',        # 주격자 점선
        gridwidth=1,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgb(230,230,230)', # 소격자 색상
            griddash='dot', # 소격자 점선
            dtick=1 # 소격자 간격 1
        ),
        range=[-10, 10]
    ),
    yaxis=dict(
        showgrid=True,
        zeroline=True,
        zerolinecolor='black', # 0점 선을 더 뚜렷하게
        zerolinewidth=2,       # 0점 선 두께
        gridcolor='lightgray',
        griddash='dot',        # 주격자 점선
        gridwidth=1,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgb(230,230,230)', # 소격자 색상
            griddash='dot', # 소격자 점선
            dtick=1 # 소격자 간격 1
        ),
        range=[-10, 10]
    ),
    height=600
)

# 스트림릿에 그래프 표시
st.plotly_chart(fig, use_container_width=True)
