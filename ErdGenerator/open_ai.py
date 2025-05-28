import openai
from dotenv import load_dotenv
import os
import base64

# api_key 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt4_vision_api(image_bytes: bytes) -> str:
    """ 이미지 데이터를 받아 미리 설정된 prompt와 함께 GPT-4 Vision API에 질의하고 응답을 반환
    Args:
        image_bytes (bytes) : 이미지 파일의 바이트 데이터
    Returns:
        str: GPT의 응답 텍스트 (DBML 코드)
    """
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    prompt = "프롬프트"

    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content