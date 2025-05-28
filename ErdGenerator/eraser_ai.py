import requests
import os
from dotenv import load_dotenv

def eraser_ai_api(prompt_text: str) -> dict:
    """ Eraser API를 통해 ERD 이미지를 생성하고, 이미지 URL과 ERD 코드만 추출하여 반환
    Args:
        prompt_text (str): 생성할 ER 다이어그램의 텍스트 프롬프트.
    Returns:
        dict: {'imageUrl': str, 'code': str}
    """
    url = "https://app.eraser.io/api/render/prompt"
    payload = {
        "diagramType": "entity-relationship-diagram",
        "mode": "standard",
        "returnFile": False,
        "background": False,
        "theme": "light",
        "text": prompt_text
    }

    # .env에서 API 토큰 로드
    load_dotenv()
    ERASER_API_TOKEN = os.getenv("ERASER_API_TOKEN")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {ERASER_API_TOKEN}"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    return {
        "imageUrl": data["imageUrl"],
        "code": data["diagrams"][0]["code"]
    }