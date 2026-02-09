import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = InferenceClient(
    model="deepseek-ai/DeepSeek-V3",
    api_key=os.getenv("HUGGING_FACE"),
)

def generate_quiz(topic: str) -> dict:
    """
    Generates 10 MCQs for a given topic
    """
    prompt = f"""
You are an expert teacher.

Generate exactly 10 multiple choice questions on:
"{topic}"

Rules:
- Medium difficulty
- 4 options per question
- Only ONE correct answer
- Output ONLY valid JSON
- No explanations
- Follow this format strictly:

{{
  "questions": [
    {{
      "question": "",
      "options": ["A) ", "B) ", "C) ", "D) "],
      "answer": "A"
    }}
  ]
}}
"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )

    raw_output = response.choices[0].message.content
    # print("\n🔹 RAW MODEL OUTPUT:\n", raw_output)

    clean_json = extract_json(raw_output)
    return clean_json


def extract_json(text: str) -> dict:

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in model output")
    
    return json.loads(match.group())

