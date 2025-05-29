from io import BytesIO
import streamlit as st
from PIL import Image
import requests
from open_ai import gpt4_vision_api
from eraser_ai import eraser_ai_api

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state["step"] = "idle"  # idle -> generating -> done
if "uploaded_img" not in st.session_state:
    st.session_state["uploaded_img"] = None
if "image_PIL" not in st.session_state:
    st.session_state["image_PIL"] = None

# Streamlit Main
st.title('⚙️ ERD Generator')
st.info(
    """
    :blue-background[**이미지 기반 ERD 자동 생성 도구**] \n
    손으로 그린 ERD 이미지를 업로드하면, 이를 기반으로 DBML 형식의 코드와 디지털 ERD 이미지를 자동으로 생성합니다.
    ERD 설계를 보다 쉽고 직관적으로 경험해보세요.
    """,
    icon="💬",
)

# 사이드바 : 이미지 업로드
st.sidebar.title("📤 이미지 업로드")
uploaded_file = st.sidebar.file_uploader(
    label="이미지 선택",
    type=["png", "jpg", "jpeg"],
    label_visibility="hidden"
)

# 샘플 이미지 사용
if st.sidebar.button("샘플 이미지 사용하기", use_container_width=True, icon=":material/image:"):
    with open("erd_sample.png", "rb") as f:
        st.session_state["uploaded_img"] = f.read()
    st.session_state["image_PIL"] = Image.open(BytesIO(st.session_state["uploaded_img"]))

# 사용자 이미지 업로드
if uploaded_file is not None:
    st.session_state["uploaded_img"] = uploaded_file.read()
    st.session_state["image_PIL"] = Image.open(BytesIO(st.session_state["uploaded_img"]))

# 이미지 미리 보기
if st.session_state["uploaded_img"] is not None:
    with st.sidebar.expander("업로드한 이미지", expanded=True):
        st.image(st.session_state["image_PIL"])

# 생성하기 버튼
if (st.session_state["uploaded_img"] is not None) and st.sidebar.button("생성하기", use_container_width=True, icon=":material/refresh:"):
    st.session_state["step"] = "generating"

# 생성
if st.session_state["step"] == "generating":
    st.warning("생성 중 ... 잠시만 기다려주세요 😊", icon=":material/hourglass_empty:")

    gpt_response = gpt4_vision_api(st.session_state["uploaded_img"])

    if gpt_response is not None:
        eraser_response = eraser_ai_api(gpt_response)
        st.session_state["generated_erd_url"] = eraser_response.get("imageUrl")
        st.session_state["generated_erd_code"] = eraser_response.get("code")
        st.session_state["step"] = "done"

# 생성된 ERD 결과 표시
if st.session_state["step"] == "done":
    try:
        response = requests.get(st.session_state["generated_erd_url"])
        response.raise_for_status()
        image_bytes = response.content

        st.success("생성이 완료되었습니다!", icon=":material/check_circle:")

        with st.container(border=True):
            st.image(st.session_state["generated_erd_url"], use_container_width=True)

        with st.expander("EraserAI ERD 코드 보기", icon=":material/code:"):
            st.code(st.session_state["generated_erd_code"], language="None")

        st.download_button(
            label="생성된 ERD 이미지 다운로드",
            data=image_bytes,
            file_name="erd_image.png",
            mime="image/png",
            icon=":material/download:"
        )

    except Exception as e:
        st.error(f"이미지를 불러오는데 실패했습니다: {e}")
