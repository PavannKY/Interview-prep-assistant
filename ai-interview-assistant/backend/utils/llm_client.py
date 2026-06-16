"""
Shared LLM client + JSON extraction helper.
Small models (phi3, qwen2.5, gemma2) don't reliably support
response_format=json_object, so we extract JSON from raw text instead.
"""
import os
import re
import json
from openai import AsyncOpenAI

def get_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "ollama"),
        base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1"),
    )

LLM_MODEL = os.getenv("LLM_MODEL", "phi3:mini")


def extract_json(text: str):
    """
    Robustly extract JSON from model output.
    Small models often wrap JSON in ```json ... ``` or add commentary.
    """
    # 1. Try raw parse first
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # 2. Extract from markdown code block
    match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3. Find first { ... } or [ ... ] block
    for pattern in (r"(\{[\s\S]+\})", r"(\[[\s\S]+\])"):
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    raise ValueError(f"Could not extract JSON from model output:\n{text[:500]}")
