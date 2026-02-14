from __future__ import annotations
import json
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
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    schema = {
        "mode": "Business Growth | Process Optimization | AI System | Education | General",
        "outline": "string",
        "script": "string",
        "shotlist": "string (exactly 5 shots, S1..S5)",
        "prompts": "string (global + per-shot prompts)",
    }

    prompt = f"""
You are an applied AI workflow engine. Return ONLY valid JSON. No markdown.

Topic: "{topic}"
Language: {language}
Platform: {platform}
Target duration: ~{duration_sec}s
Audience: {audience}
Style preset: {style_preset}

Requirements:
- Make outputs highly topic-specific (avoid generic templates).
- Outline: 5 beats, clear and practical.
- Script: short sentences, production-ready pacing.
- Shotlist: exactly 5 shots, label S1..S5 with camera+action.
- Prompt pack: global look + per-shot prompts; avoid readable text artifacts.

Return JSON with keys exactly:
{json.dumps(schema, ensure_ascii=False)}

Now output the JSON:
"""

    resp = model.generate_content(prompt)
    text = (resp.text or "").strip()

    # Robust JSON parse
    try:
        data = json.loads(text)
    except Exception:
        text2 = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text2)

    return {
        "mode": data.get("mode", "General"),
        "outline": data.get("outline", ""),
        "script": data.get("script", ""),
        "shotlist": data.get("shotlist", ""),
        "prompts": data.get("prompts", ""),
    }
