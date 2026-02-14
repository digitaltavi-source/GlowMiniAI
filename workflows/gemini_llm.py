from __future__ import annotations
import os, json
from typing import Dict, Any

def gemini_generate_pack(
    api_key: str,
    topic: str,
    language: str,
    platform: str,
    duration_sec: int,
    audience: str,
    style_preset: str,
) -> Dict[str, Any]:
    """
    Returns dict with keys: outline, script, shotlist, prompts, mode, meta
    """
    import google.generativeai as genai

    genai.configure(api_key=api_key)

    # You can switch to a newer model later; keep stable for now.
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Force structured JSON so outputs are consistent and usable.
    system = (
        "You are an applied AI creative workflow engine. "
        "Return ONLY valid JSON. No markdown. No extra text."
    )

    schema = {
        "mode": "string (one of: Business Growth, Process Optimization, AI System, Education, General)",
        "outline": "string",
        "script": "string",
        "shotlist": "string",
        "prompts": "string",
        "meta": {"notes": "string"},
    }

    prompt = f"""
SYSTEM: {system}

TASK:
Generate a high-quality, topic-specific pack for: "{topic}"

CONSTRAINTS:
- Language: {language}
- Platform: {platform}
- Duration: about {duration_sec} seconds
- Audience: {audience}
- Visual style preset: {style_preset}
- Make it clearly different depending on topic (avoid generic templates).
- Script must be short sentences, production-friendly timing.
- Shotlist: exactly 5 shots, each with camera + action.
- Prompt pack: Global look + per-shot prompts; avoid readable text artifacts.

OUTPUT FORMAT:
Return JSON exactly matching this schema (keys must exist):
{json.dumps(schema, ensure_ascii=False)}

Now produce the JSON:
"""

    resp = model.generate_content(prompt)
    text = resp.text.strip()

    # Safety: parse JSON robustly
    try:
        data = json.loads(text)
    except Exception:
        # If model wraps JSON in code fences, strip them
        text2 = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text2)

    return {
        "mode": data.get("mode", "LLM"),
        "outline": data.get("outline", ""),
        "script": data.get("script", ""),
        "shotlist": data.get("shotlist", ""),
        "prompts": data.get("prompts", ""),
        "meta": {"llm": "gemini-1.5-flash", "notes": (data.get("meta") or {}).get("notes", "")},
    }
