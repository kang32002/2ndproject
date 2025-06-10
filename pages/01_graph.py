import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("일차방정식 $x=m$, $y=n$의 지도 시각화")
st.write("Plotly를 이용하여 입력받은 $m$과 $n$ 값에 해당하는 경도 및 위도 선을 지도에 표시합니다.")

# 사용자로부터 m과 n 값 입력받기
col1, col2 = st.columns(2)
with col1:
    m = st.number_input("x 값 (경도, longitude)을 입력하세요:", value=127.0, format="%.4f")
with col2:
    n = st.number_input("y 값 (위도, latitude)을 입력하세요:", value=37.5, format="%.4f")

st.markdown(f"입력된 값: $x = {m}$, $y = {n}$")

# Plotly 지도 생성
fig = go.Figure()

# x = m (경도) 선 그리기
# 경도선은 북극(-90)부터 남극(90)까지 이어집니다.
fig.add_trace(
    go.Scattergeo(
        lon=[m, m],
        lat=[-90, 90],
        mode='lines',
        line=dict(color='red', width=2),
        name=f'x = {m} (경도선)'
    )
)

# y = n (위도) 선 그리기
# 위도선은 전 세계를 가로지르므로 -180부터 180까지 이어집니다.
fig.add_trace(
    go.Scattergeo(
        lon=[-180, 180],
        lat=[n, n],
        mode='lines',
        line=dict(color='blue', width=2),
        name=f'y = {n} (위도선)'
    )
)

# 지도 레이아웃 설정
fig.update_layout(
    geo_scope='world',  # 전 세계 지도
    geo=dict(
        showland=True,
        landcolor="rgb(243, 243, 243)",
        countrycolor="rgb(204, 204, 204)",
        showocean=True,
        oceancolor="rgb(180, 210, 230)",
        showlakes=True,
        lakecolor="rgb(180, 210, 230)",
        resolution=50,  # 지도 해상도 (110m, 50m, 10m)
        center=dict(lon=m, lat=n), # 입력된 m, n 값에 지도의 중심을 맞춤
        projection_scale=1.5 # 지도 확대/축소
    ),
    title_text="일차방정식 $x=m$, $y=n$의 지도 시각화",
    height=700
)

# 스트림릿에 지도 표시
st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.write("### 설명")
st.write(f"- 빨간색 선은 $x = {m}$ (경도선)을 나타냅니다.")
st.write(f"- 파란색 선은 $y = {n}$ (위도선)을 나타냅니다.")
st.write("- 대한민국 서울의 대략적인 위도와 경도는 각각 37.5와 127.0 입니다. 기본값으로 설정되어 있습니다.")
