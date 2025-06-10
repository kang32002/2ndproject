import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

st.title("일차방정식 $ax + by + c = 0$ 그래프 시각화")
st.write("Plotly를 이용하여 입력받은 $a$, $b$, $c$ 값에 해당하는 직선을 좌표평면에 표시합니다.")

# 사용자로부터 a, b, c 값 입력받기
col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input("a 값을 입력하세요:", value=1.0, format="%.2f")
with col2:
    b = st.number_input("b 값을 입력하세요:", value=-1.0, format="%.2f")
with col3:
    c = st.number_input("c 값을 입력하세요:", value=0.0, format="%.2f")

st.markdown(f"입력된 방정식: ${a}x + {b}y + {c} = 0$")

# 그래프 그리기 위한 x, y 값 계산
# ax + by + c = 0 에서 y를 x에 대한 식으로 정리
# by = -ax - c
# y = (-a/b)x - (c/b)   (단, b가 0이 아닐 때)

# x 값 범위 설정
x = np.linspace(-10, 10, 400) # -10부터 10까지 400개의 점 생성

fig = go.Figure()

# Plotly 그래프 생성
if b == 0:
    # by + c = 0 이므로, a가 0이 아니면 ax + c = 0 즉 x = -c/a (수직선)
    if a != 0:
        x_val = -c / a
        # 수직선은 x 값이 고정, y는 범위 내에서 변동
        fig.add_trace(
            go.Scatter(
                x=[x_val, x_val],
                y=[-10, 10], # y축 범위에 맞게 설정
                mode='lines',
                name=f'$x = {-c/a}$',
                line=dict(color='red', width=3)
            )
        )
        st.write(f"이는 수직선 $x = {-c/a}$ 입니다.")
    else:
        # a=0, b=0 일 경우 (c=0 이면 모든 점, c!=0 이면 그래프 없음)
        if c == 0:
            st.warning("방정식 $0x + 0y + 0 = 0$은 모든 실수 x, y에 대해 성립하므로, 좌표평면 전체를 나타냅니다.")
        else:
            st.error(f"방정식 $0x + 0y + {c} = 0$은 성립하지 않으므로, 그래프가 존재하지 않습니다.")
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
            name=f'${a}x + {b}y + {c} = 0$',
            line=dict(color='blue', width=3)
        )
    )
    if a == 0:
        st.write(f"이는 수평선 $y = {-c/b}$ 입니다.")


# 그래프 레이아웃 설정
fig.update_layout(
    title=f"직선 ${a}x + {b}y + {c} = 0$",
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
        range=[-10, 10] # y축 범위 설정
    ),
    height=600
)

# 스트림릿에 그래프 표시
st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.write("### 설명")
st.write(f"- 입력된 계수 $a$, $b$, $c$에 따라 방정식 $ax + by + c = 0$의 그래프를 그립니다.")
st.write("- **$b \neq 0$** 일 때: $y = (-\frac{a}{b})x - (\frac{c}{b})$ 형태로 변환하여 일반적인 직선을 그립니다.")
st.write("  - 이때 $\\left(-\\frac{a}{b}\\right)$는 직선의 **기울기**가 되고, $\\left(-\\frac{c}{b}\\right)$는 **y절편**이 됩니다.")
st.write("- **$b = 0$** 이고 **$a \neq 0$** 일 때: $ax + c = 0$ 이므로 $x = -\frac{c}{a}$ (수직선)을 그립니다.")
st.write("- **$a = 0$** 이고 **$b = 0$** 일 때:")
st.write("  - **$c = 0$** 이면: $0x + 0y + 0 = 0$이므로 모든 실수 $x, y$에 대해 성립하는 **좌표평면 전체**를 나타냅니다.")
st.write("  - **$c \neq 0$** 이면: $0x + 0y + c = 0$은 성립하지 않으므로 **그래프가 존재하지 않습니다**.")
