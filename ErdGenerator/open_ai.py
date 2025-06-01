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

    prompt = """
        이 이미지를 보고 erd를 DBML 코드로 변환해줘.
        Table의 예시 코드는 아래와 같아 :
            Table users {
              id integer [primary key]
              username varchar
              role varchar
              created_at timestamp
            }
        Ref의 예시 코드를 아래와 같아:
            Ref user_posts: posts.user_id > users.id // many-to-one
            Ref: users.id < follows.following_user_id
        
        답변은 DBML(Table과 ref를 포함한) 코드만 포함해줘.
    """

    response = openai.chat.completions.create(
        model="gpt-4o",
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

    print("✅ GPT response \n", response)

    return response.choices[0].message.content
