import streamlit as st
from PIL import Image
import requests
from open_ai import gpt4_vision_api
from eraser_ai import eraser_ai_api

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state["step"] = "idle"  # idle -> generating -> done

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
uploaded_img = st.sidebar.file_uploader(
    label="이미지 선택",
    type=["png", "jpg", "jpeg"],
    label_visibility="hidden"
)
if uploaded_img is not None:
    image = Image.open(uploaded_img)
    with st.sidebar.expander("업로드한 이미지", expanded=True):
        st.image(image)
    if st.sidebar.button("생성하기", use_container_width=True, icon=":material/refresh:"):
        st.session_state["step"] = "generating"


# GPT-4 Vision API
if st.session_state["step"] == "generating":
    warning = st.warning(
        """
        생성 중 ... 잠시만 기다려주세요 😊
        """,
        icon=":material/hourglass_empty:"
    )

    # gpt_response = gpt4_vision_api(uploaded_img)
    gpt_response = "123"

    # Eraser API
    if gpt_response is not None:
        # eraser_response = eraser_ai_api(gpt_response)
        # generated_erd_url = eraser_response.get("imageUrl")
        # generated_erd_code = eraser_response.get("code")
        st.session_state["step"] = "done"


# # 더미데이터
st.session_state["generated_erd_url"] = "https://image.utoimage.com/preview/cp872722/2022/12/202212008462_500.jpg"
generated_erd_code = """
// title\ntitle Social Media Platform Data Model\n\n
// define tables\nusers [icon: user, color: yellow]{\n  id string pk\n  username string unique\n  email string\n  password string\n  createdAt timestamp\n}\n\n
tweets [icon: message-square, color: blue]{\n  id string pk\n  userId string\n  content string\n  createdAt timestamp\n}\n\n
comments [icon: message-circle, color: green]{\n  id string pk\n  userId string\n  content string\n  createdAt timestamp\n  tweetId string\n}\n\n
likes [icon: heart, color: red]{\n  id string pk\n  createdAt timestamp\n  userId string\n  tweetId string\n}\n\n
followers [icon: users, color: purple]{\n  id string pk\n  followerId string\n  followeeId string\n}\n\n
// define relationships\ntweets.userId > users.id\ncomments.userId > users.id\ncomments.tweetId > tweets.id\nlikes.userId > users.id\nlikes.tweetId > tweets.id\nfollowers.followerId > users.id\nfollowers.followeeId > users.id\n
"""


# 생성된 이미지 부분
if st.session_state["step"] == "done":
    try:
        response = requests.get(st.session_state["generated_erd_url"] )
        response.raise_for_status()
        image_bytes = response.content

        warning.empty()
        st.success(
            """
            생성이 완료되었습니다!
            """,
            icon=":material/check_circle:"
        )

        with st.container(border=True):
            st.image(st.session_state["generated_erd_url"], use_container_width=True)

        with st.expander("EraserAI ERD 코드 보기", icon=":material/code:"):
            st.code(generated_erd_code, language="None")

        st.download_button(
            label="생성된 ERD 이미지 다운로드",
            data=image_bytes,
            file_name="erd_image.png",
            mime="image/png",
            icon=":material/download:"
        )

    except Exception as e:
        st.error(f"이미지를 불러오는데 실패했습니다: {e}")
