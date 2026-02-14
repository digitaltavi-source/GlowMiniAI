from __future__ import annotations
import os, json, random, datetime
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class WorkflowResult:
    topic: str
    language: str
    platform: str
    duration_sec: int
    audience: str
    style_preset: str
    outline: str
    script: str
    shotlist: str
    prompts: str
    meta: Dict[str, Any]

def _now_stamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def _safe_name(s: str, max_len: int = 50) -> str:
    safe = "".join([c for c in s if c.isalnum() or c in (" ", "_", "-", ".")]).strip().replace(" ", "_")
    return safe[:max_len] if safe else "pack"

def _pick(options: List[str]) -> str:
    return random.choice(options)

def _style_bank(style_preset: str) -> Dict[str, str]:
    bank = {
        "Cinematic 3D": {
            "global": "cinematic stylized 3D, shallow depth of field, warm highlights, soft rim light, clean composition, high clarity",
            "lighting": "soft key light + warm rim light, gentle bloom, controlled shadows",
            "lens": "35mm–50mm, shallow DOF",
        },
        "Clean Minimal": {
            "global": "minimal 3D, bright studio lighting, simple shapes, high readability, clean background",
            "lighting": "even studio softbox, low contrast, high clarity",
            "lens": "35mm, medium DOF",
        },
        "Handcrafted Cozy": {
            "global": "handcrafted 3D look, gentle textures, cozy mood, warm palette, family-friendly",
            "lighting": "warm ambient, soft fill, subtle vignette",
            "lens": "50mm, soft DOF",
        },
        "Tech Explainer": {
            "global": "modern tech explainer style, clean UI overlays (no text artifacts), schematic icons, crisp edges, professional",
            "lighting": "neutral studio light, balanced contrast",
            "lens": "35mm, medium DOF",
        },
    }
    return bank.get(style_preset, bank["Cinematic 3D"])

def generate_media_pack(
    topic: str,
    language: str = "vi",
    platform: str = "YouTube Shorts",
    duration_sec: int = 35,
    audience: str = "General",
    style_preset: str = "Cinematic 3D",
    seed: Optional[int] = None,
) -> WorkflowResult:
    """
    Offline/mock generator that produces practical outputs:
    - Outline (hook + beats)
    - Script (time-boxed)
    - Shotlist (5 shots)
    - Prompt pack (global + per-shot)
    Designed to run WITHOUT API keys.
    """

    if seed is not None:
        random.seed(seed)

    style = _style_bank(style_preset)

    hooks_vi = [
        "Chỉ {t}s để hiểu điều quan trọng về “{topic}”.",
        "Một điều nhỏ xíu… nhưng có thể thay đổi cách bạn làm “{topic}”.",
        "Nếu bạn hay bị rối vì “{topic}”, đây là 1 cách gỡ nhanh.",
        "Mình dùng 1 mẹo đơn giản để làm “{topic}” gọn hơn rất nhiều.",
    ]
    hooks_en = [
        "{t}s to understand what matters about “{topic}”.",
        "A tiny shift that changes how you handle “{topic}”.",
        "If “{topic}” feels messy, here’s a quick unlock.",
        "One simple method to make “{topic}” much cleaner.",
    ]

    beats_vi = [
        "Mở cảnh gần gũi → nêu vấn đề",
        "Chỉ ra điểm nghẽn (1 câu)",
        "Bật mí nguyên tắc cốt lõi",
        "Hành động 1 bước (làm ngay)",
        "Kết: khích lệ + bước tiếp theo",
    ]
    beats_en = [
        "Relatable opening → state the problem",
        "Show the bottleneck (one line)",
        "Reveal the core principle",
        "One-step action (do it today)",
        "Close: encouragement + next step",
    ]

    cta_vi = "Nếu bạn muốn, mình có thể giúp bạn biến nó thành workflow rõ ràng hơn."
    cta_en = "If you want, I can help turn this into a clearer workflow."

    hook = _pick(hooks_vi if language.startswith("vi") else hooks_en).format(topic=topic, t=duration_sec)
    beats = beats_vi if language.startswith("vi") else beats_en
    cta = cta_vi if language.startswith("vi") else cta_en

    outline = f"""HOOK: {hook}

STRUCTURE (5 beats):
1) {beats[0]}
2) {beats[1]}
3) {beats[2]}
4) {beats[3]}
5) {beats[4]}

TARGET: {platform} | Duration: ~{duration_sec}s | Audience: {audience}
"""

    # Practical script: time-boxed, short sentences, production-friendly
    script = f"""[{language.upper()} SCRIPT — ~{duration_sec}s | {platform}]
{hook}

(1) Mình bắt đầu với “{topic}” bằng cách bỏ bớt cái thừa.
(2) Điểm nghẽn thường là: làm quá nhiều thứ cùng lúc.
(3) Nguyên tắc: chia nhỏ thành 3 phần — Input → Process → Output.
(4) Bước làm ngay: chọn 1 output duy nhất, rồi quay ngược để biết cần input gì.
(5) {cta}
"""

    # Shotlist: production-friendly instructions
    camera_moves = ["slow dolly in", "gentle pan", "top-down reveal", "over-shoulder close-up", "wide establishing shot"]
    props = ["notebook", "sticky notes", "simple dashboard", "workflow board", "clean desk setup"]
    metaphors = ["one clear arrow", "a single checklist", "three-step pipeline", "before/after board", "time-box timer"]

    move1 = _pick(camera_moves)
    move2 = _pick(camera_moves)
    move3 = _pick(camera_moves)
    move4 = _pick(camera_moves)
    move5 = _pick(camera_moves)

    shotlist = f"""SHOTLIST (5 shots)
S1 Hook: {move1} | close-up | prop: {_pick(props)} | metaphor: {_pick(metaphors)}
S2 Problem: {move2} | medium | show clutter / overload
S3 Insight: {move3} | insert | reveal "Input→Process→Output" as a visual concept (no readable text required)
S4 Action: {move4} | hands-on | demonstrate 1-step: pick one output → work backward
S5 Close: {move5} | wide | calm workspace, hopeful mood, subtle smile
"""

    # Prompt pack: usable across image/video tools
    prompts = f"""[PROMPT PACK — API-free offline draft]
GLOBAL LOOK:
- {style['global']}
- lighting: {style['lighting']}
- lens: {style['lens']}
- family-friendly, professional, no gore, no explicit content
- avoid readable text artifacts, avoid watermark/logo artifacts
- consistent character style & color palette

SCENE CONTEXT:
- Topic: "{topic}"
- Platform: {platform} | Duration: ~{duration_sec}s | Audience: {audience}

SHOT 1 (Hook):
{style['global']}, {style['lighting']}, {move1}, close-up, {_pick(props)}, emotional but subtle, clean background

SHOT 2 (Problem):
{style['global']}, {style['lighting']}, {move2}, medium shot, visual clutter, overwhelmed gesture, clear storytelling

SHOT 3 (Insight):
{style['global']}, {style['lighting']}, {move3}, insert shot, reveal a simple 3-step pipeline concept (Input→Process→Output) via shapes/icons, no readable text

SHOT 4 (Action):
{style['global']}, {style['lighting']}, {move4}, hands arranging steps, single checklist, confident pacing

SHOT 5 (Close):
{style['global']}, {style['lighting']}, {move5}, wide shot, calm workspace, warm hopeful mood, gentle smile
"""

    meta = {
        "generated_at": _now_stamp(),
        "mode": "offline_mock",
        "seed": seed,
        "style_preset": style_preset,
        "platform": platform,
        "duration_sec": duration_sec,
        "audience": audience,
    }

    return WorkflowResult(
        topic=topic,
        language=language,
        platform=platform,
        duration_sec=duration_sec,
        audience=audience,
        style_preset=style_preset,
        outline=outline,
        script=script,
        shotlist=shotlist,
        prompts=prompts,
        meta=meta,
    )

def save_pack(result: WorkflowResult, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    stamp = result.meta.get("generated_at") or _now_stamp()
    fname = f"{stamp}_{_safe_name(result.topic)}.md"
    path = os.path.join(out_dir, fname)

    content = f"""# GlowMiniAI Output Pack (v1.2)
Topic: {result.topic}
Language: {result.language}
Platform: {result.platform}
Duration: {result.duration_sec}s
Audience: {result.audience}
Style: {result.style_preset}
Generated: {result.meta.get('generated_at')}
Mode: {result.meta.get('mode')}

## Outline
{result.outline}

## Script
{result.script}

## Shotlist
{result.shotlist}

## Prompt Pack
{result.prompts}

## Meta
{json.dumps(result.meta, ensure_ascii=False, indent=2)}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path