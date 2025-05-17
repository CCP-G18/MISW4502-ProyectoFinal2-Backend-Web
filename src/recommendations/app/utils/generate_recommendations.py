import os
import base64
from openai import OpenAI
import httpx
import mimetypes

def ask_gpt_with_images(image_paths: list[str], prompt: str):
    client = get_openai_client()
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

    for path in image_paths:
        mime_type, _ = mimetypes.guess_type(path)
        if not mime_type:
            mime_type = "image/jpeg"
        with open(path, "rb") as f:
            base64_img = base64.b64encode(f.read()).decode()
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_img}"
                }
            })

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message.content

def get_openai_client():
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"], http_client=httpx.Client(verify=False))