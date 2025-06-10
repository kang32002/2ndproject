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

---

### **설명**

이 앱은 일차방정식 **<span class="math-inline">ax \+ by \+ c \= 0</span>** 의 그래프를 좌표평면에 시각화합니다. 사용자가 입력하는 계수 **<span class="math-inline">a, b, c</span>** 값에 따라 직선의 형태가 달라집니다.

---

### **축 및 격자 설정**

* **x축과 y축 (<span class="math-inline">x\=0</span>, <span class="math-inline">y\=0</span>)**: 검은색으로 뚜렷하게 표시되어 있습니다.
* **주격자**: 연한 회색 점선으로 표시됩니다.
* **소격자**: 각 축에서 간격 **1**마다 더 연한 회색 점선으로 표시되어, 좌표를 읽기 편리하도록 돕습니다.

---

### **<span class="math-inline">a, b, c</span> 값에 따른 그래프 변화**

일차방정식 <span class="math-inline">ax \+ by \+ c \= 0</span>은 <span class="math-inline">a, b</span> 값에 따라 다음과 같은 특성을 가집니다.

* **1. <span class="math-inline">b \\neq 0</span> 인 경우 (일반적인 기울기를 가진 직선)**
    * 방정식을 <span class="math-inline">y</span>에 대해 정리하면 <span class="math-inline">y \= \\left\(\-\\frac\{a\}\{b\}\\right\)x \- \\left\(\\frac\{c\}\{b\}\\right\)</span> 형태가 됩니다.
    * 여기서 <span class="math-inline">\\left\(\-\\frac\{a\}\{b\}\\right\)</span>는 직선의 **기울기**를 나타내며, <span class="math-inline">\\left\(\-\\frac\{c\}\{b\}\\right\)</span>는 **y절편**이 됩니다.
    * **예시**: <span class="math-inline">a\=1, b\=\-1, c\=0</span> (즉, <span class="math-inline">x \- y \= 0 \\Rightarrow y \= x</span>)을 입력하면 기울기가 1인 직선이 그려집니다.

* **2. <span class="math-inline">b \= 0</span> 이고 <span class="math-inline">a \\neq 0</span> 인 경우 (수직선)**
    * 방정식은 <span class="math-inline">ax \+ c \= 0</span> 형태가 됩니다.
    * 이를 <span class="math-inline">x</span>에 대해 정리하면 <span class="math-inline">x \= \-\\frac\{c\}\{a\}</span> 가 되며, 이는 **x축에 수직인 직선**을 나타냅니다. (예: <span class="math-inline">x\=3</span>)
    * 이 경우 그래프는 **빨간색**으로 표시됩니다.
    * **예시**: <span class="math-inline">a\=1, b\=0, c\=\-3</span> (즉, <span class="math-inline">x \- 3 \= 0 \\Rightarrow x \= 3</span>)을 입력하면 <span class="math-inline">x\=3</span>을 지나는 수직선이 그려집니다.

* **3. <span class="math-inline">a \= 0</span> 이고 <span class="math-inline">b \\neq 0</span> 인 경우 (수평선)**
    * 방정식은 <span class="math-inline">by \+ c \= 0</span> 형태가 됩니다.
    * 이를 <span class="math-inline">y</span>에 대해 정리하면 <span class="math-inline">y \= \-\\frac\{c\}\{b\}</span> 가 되며, 이는 **y축에 수직인 직선** (즉, x축에 평행한 수평선)을 나타냅니다. (예: <span class="math-inline">y\=2</span>)
    * 이 경우 그래프는 **파란색**으로 표시됩니다. (첫 번째 경우의 특별한 케이스로 처리되어 파란색으로 그려집니다.)
    * **예시**: <span class="math-inline">a\=0, b\=1, c\=\-2</span> (즉, <span class="math-inline">y \- 2 \= 0 \\Rightarrow y \= 2</span>)를 입력하면 <span class="math-inline">y\=2</span>를 지나는 수평선이 그려집니다.

* **4. <span class="math-inline">a \= 0</span> 이고 <span class="math-inline">b \= 0</span> 인 경우 (특수 케이스)**
    * 방정식은 <span class="math-inline">0x \+ 0y \+ c \= 0</span> 형태가 됩니다.
    * **<span class="math-inline">c \= 0</span> 이면**: <span class="math-inline">0x \+ 0y \+ 0 \= 0</span> (즉, <span class="math-inline">0 \= 0</span>)이 되어 **모든 실수 <span class="math-inline">x, y</span>에 대해 항상 성립**합니다. 이는 **좌표평면 전체**를 의미합니다.
    * **<span class="math-inline">c \\neq 0</span> 이면**: <span class="math-inline">0x \+ 0y \+ c \= 0</span> (예: <span class="math-inline">0x \+ 0y \+ 5 \= 0 \\Rightarrow 5 \= 0</span>)은 **성립하지 않습니다**. 따라서 이 방정식을 만족하는 **그래프는 존재하지 않습니다.**

---

이 개선된 코드를 통해 일차방정식의 시각화가 훨씬 명확해지고, 다양한 특수 케이스에 대한 이해를 높일 수 있을 것입니다.

궁금한 점이나 추가하고 싶은 기능이 있으신가요?
