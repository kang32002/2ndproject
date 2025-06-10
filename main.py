import streamlit as st
import folium
from streamlit_folium import st_folium

# 관광지 데이터
tourist_spots = {
    "도쿄 - 도쿄타워": {
        "lat": 35.6586,
        "lon": 139.7454,
        "description": "도쿄타워는 도쿄의 대표적인 랜드마크로, 전망대에서는 도쿄 전경을 한눈에 볼 수 있습니다. 밤에는 아름다운 조명으로 유명합니다."
    },
    "교토 - 기요미즈데라(청수사)": {
        "lat": 34.9949,
        "lon": 135.7850,
        "description": "기요미즈데라는 일본 교토에 위치한 고대 사찰로, 벚꽃과 단풍 시즌에 특히 아름답습니다. 절벽 위의 목조건물과 풍경이 인상적입니다."
    },
    "오사카 - 오사카성": {
        "lat": 34.6873,
        "lon": 135.5259,
        "description": "도요토미 히데요시가 지은 역사적인 성으로, 일본 역사에 큰 의미를 지닌 명소입니다. 주변 공원도 산책하기 좋습니다."
    },
    "히로시마 - 원폭 돔": {
        "lat": 34.3955,
        "lon": 132.4536,
        "description": "제2차 세계대전 당시 원자폭탄 투하의 흔적을 간직한 건축물로, 평화의 소중함을 일깨워주는 장소입니다."
    },
    "삿포로 - 오도리 공원": {
        "lat": 43.0618,
        "lon": 141.3545,
        "description": "삿포로 중심부에 위치한 대형 공원으로, 겨울철 눈축제로 유명합니다. 다양한 이벤트와 조형물이 매력적입니다."
    }
}

# Streamlit UI
st.set_page_config(page_title="일본 관광 가이드", layout="wide")
st.title("🇯🇵 일본 주요 관광지 가이드")
st.markdown("일본의 아름다운 도시와 관광지를 자세히 살펴보세요. 관광지를 선택하면 지도와 함께 설명이 표시됩니다.")

# 관광지 선택
selected_spot = st.selectbox("관광지를 선택하세요:", list(tourist_spots.keys()))

# 선택된 관광지 정보
spot = tourist_spots[selected_spot]
st.subheader(f"📍 {selected_spot}")
st.write(spot["description"])

# 지도 표시
m = folium.Map(location=[spot["lat"], spot["lon"]], zoom_start=15)
folium.Marker([spot["lat"], spot["lon"]], tooltip=selected_spot, popup=spot["description"]).add_to(m)

# Streamlit에 지도 렌더링
st_folium(m, width=700, height=500)
