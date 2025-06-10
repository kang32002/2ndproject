import streamlit as st
import folium
from streamlit_folium import st_folium
import random # random 모듈 추가

# 관광지 정보 데이터
tourist_data = {
    "도쿄 - 도쿄타워": {
        "lat": 35.6586,
        "lon": 139.7454,
        "description": "도쿄타워는 도쿄의 대표적인 랜드마크로, 전망대에서는 도쿄 전경을 한눈에 볼 수 있습니다.",
        "food": ["스시잔마이 도쿄본점 🍣", "잇푸도 라멘 시바 공원점 🍜", "텐야 텐푸라 ⛩️"],
        "hotels": ["더 프린스 파크타워 도쿄 🏨", "ANA 인터컨티넨탈 도쿄 🌟", "신주쿠 워싱턴 호텔 📍"],
        "transport": "하마마츠초역 또는 아카바네바시역에서 도보 5~10분 거리입니다.",
        "youtube": "https://www.youtube.com/watch?v=M9U_zX95t3k", # 실제 유튜브 링크 예시
        "link": "https://www.tokyotower.co.jp/"
    },
    "교토 - 기요미즈데라(청수사)": {
        "lat": 34.9949,
        "lon": 135.7850,
        "description": "기요미즈데라는 교토의 대표 사찰로, 전통적인 건축양식과 아름다운 경치로 유명합니다.",
        "food": ["기온 스이렌 가이세키 요리 🍱", "야사카만주 찻집 🍡", "이치란 라멘 🍜"],
        "hotels": ["교토 호텔 오쿠라 🏯", "기온 하나레 료칸 ✨", "호텔 그랑비아 교토 🚅"],
        "transport": "기온시조역 또는 기요미즈고조역에서 도보 10~15분 거리입니다.",
        "youtube": "https://www.youtube.com/watch?v=l_G2807jX7Q", # 실제 유튜브 링크 예시
        "link": "https://www.kiyomizudera.or.jp/"
    },
    "오사카 - 오사카성": {
        "lat": 34.6873,
        "lon": 135.5259,
        "description": "도요토미 히데요시가 지은 오사카성은 역사와 풍경이 어우러진 관광 명소입니다.",
        "food": ["다루마 꼬치튀김 🍢", "미즈노 오코노미야키 🍳", "이치란 라멘 난바점 🍜"],
        "hotels": ["호텔 뉴 오타니 오사카 🏨", "스위소텔 난카이 오사카 💼", "도톤보리 호텔 🎭"],
        "transport": "오사카 비즈니스 파크역에서 도보 10분 거리입니다.",
        "youtube": "https://www.youtube.com/watch?v=S2g3w9gZ0_0", # 실제 유튜브 링크 예시
        "link": "https://www.osakacastle.net/"
    },
    "히로시마 - 원폭 돔": {
        "lat": 34.3955,
        "lon": 132.4536,
        "description": "평화기념공원 내 원폭 돔은 전쟁의 비극과 평화의 중요성을 일깨워줍니다.",
        "food": ["오코노미무라 히로시마풍 오코노미야키 🍳", "이쿠로 라멘 🍜", "카페 폰토 🌸"],
        "hotels": ["리버사이드 호텔 히로시마 🏨", "호텔 그란비아 히로시마 🚄", "ANA 크라운 플라자 히로시마 🌟"],
        "transport": "히로시마역에서 노면전차(덴샤)를 타고 '겐바쿠 돔마에'에서 하차합니다.",
        "youtube": "https://www.youtube.com/watch?v=Vl3s_e7W6vM", # 실제 유튜브 링크 예시
        "link": "https://hpmmuseum.jp/?lang=en"
    },
    "삿포로 - 오도리 공원": {
        "lat": 43.0618,
        "lon": 141.3545,
        "description": "삿포로 눈 축제로 유명한 오도리 공원은 사계절 내내 활기찬 도심 속 쉼터입니다.",
        "food": ["스스키노 징기스칸 야키니쿠 🍖", "스프 카레 가라쿠 🍛", "삿포로 클래식 맥주 펍 🍺"],
        "hotels": ["삿포로 그랜드 호텔 🏔️", "호텔 몬트레 삿포로 🌨️", "JR 타워 호텔 닛코 삿포로 🚉"],
        "transport": "오도리역에서 도보 1분 거리로 매우 가까운 위치에 있습니다.",
        "youtube": "https://www.youtube.com/watch?v=zR2R41hFvK4", # 실제 유튜브 링크 예시
        "link": "https://www.sapporo-odori.jp/"
    }
}

# 페이지 설정
st.set_page_config(page_title="일본 관광 가이드", layout="wide")
st.title("🇯🇵 일본 주요 관광지 가이드")
st.markdown("관광지를 선택하면 소개 정보, 유튜브 영상, 지도, 맛집, 호텔, 교통 안내 및 공식 사이트 링크가 표시됩니다.")

# 세션 상태(Session State) 초기화 및 사용
if "selected_spot" not in st.session_state:
    st.session_state.selected_spot = None

# 관광지 선택 버튼 UI
cols = st.columns(len(tourist_data.keys())) # 모든 관광지 버튼을 한 줄에 배치 (옵션)
for idx, spot in enumerate(tourist_data.keys()):
    if cols[idx].button(spot, key=spot):
        st.session_state.selected_spot = spot

# '결정해줘!' 버튼 추가
st.markdown("---") # 구분선 추가
if st.button("결정해줘!", key="random_button", type="primary"): # type="primary"로 파란색 배경 설정
    random_spot = random.choice(list(tourist_data.keys()))
    st.session_state.selected_spot = random_spot

# 선택된 관광지 정보 출력
if st.session_state.selected_spot:
    selected = st.session_state.selected_spot
    data = tourist_data[selected]
    st.header(f"📍 {selected}")
    st.write(data["description"])

    # 공식 사이트
    st.markdown(f"[🌐 공식 사이트 바로가기]({data['link']})")

    # YouTube 영상
    st.subheader("🎥 소개 영상")
    st.video(data["youtube"])

    # 지도
    m = folium.Map(location=[data["lat"], data["lon"]], zoom_start=15)
    folium.Marker([data["lat"], data["lon"]], tooltip=selected, popup=data["description"]).add_to(m)
    st.subheader("🗺️ 위치 지도")
    st_folium(m, width=700, height=500)

    # 맛집
    st.subheader("🍽️ 추천 맛집")
    for r in data["food"]:
        st.markdown(f"- {r}")

    # 호텔
    st.subheader("🏨 추천 호텔")
    for h in data["hotels"]:
        st.markdown(f"- {h}")

    # 교통 안내
    st.subheader("🚉 교통 안내")
    st.write(data["transport"])
else:
    st.info("상단의 관광지 버튼 또는 '결정해줘!' 버튼을 클릭해 정보를 확인해보세요.")
