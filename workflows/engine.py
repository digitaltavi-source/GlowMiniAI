from __future__ import annotations
import os, json, random, datetime, re
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
    mode: str
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
            "global": "modern tech explainer style, schematic icons, crisp edges, professional, avoid readable text artifacts",
            "lighting": "neutral studio light, balanced contrast",
            "lens": "35mm, medium DOF",
        },
    }
    return bank.get(style_preset, bank["Cinematic 3D"])

def _detect_mode(topic: str) -> str:
    t = topic.lower()
    # simple keyword routing (A-level: lightweight + robust)
    if re.search(r"\b(doanh thu|bán|marketing|ads|quảng cáo|shop|sàn|shopee|tiktok|funnel|conversion|khách hàng)\b", t):
        return "Business Growth"
    if re.search(r"\b(quy trình|tối ưu|workflow|process|vận hành|sop|kpi|chi phí|tự động|automation)\b", t):
        return "Process Optimization"
    if re.search(r"\b(ai|machine learning|ml|data|dữ liệu|api|system|hệ thống|pipeline|agent)\b", t):
        return "AI System"
    if re.search(r"\b(học|giáo dục|dạy|đào tạo|lesson|kids|trẻ em)\b", t):
        return "Education"
    return "General"

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
    Offline/mock generator with lightweight adaptive modes.
    Produces practical outputs:
    - Outline (mode-specific beats)
    - Script (mode-specific structure)
    - Shotlist (5 shots)
    - Prompt pack (global + per-shot)
    Runs WITHOUT API keys.
    """
    if seed is not None:
        random.seed(seed)

    style = _style_bank(style_preset)
    mode = _detect_mode(topic)

    camera_moves = ["slow dolly in", "gentle pan", "top-down reveal", "over-shoulder close-up", "wide establishing shot"]
    props = ["notebook", "sticky notes", "simple dashboard", "workflow board", "clean desk setup", "product box", "phone screen mockup"]
    metaphors = ["one clear arrow", "a single checklist", "three-step pipeline", "before/after board", "time-box timer", "simple funnel"]

    # Hooks
    hooks_vi = {
        "Business Growth": [
            "Muốn tăng doanh thu từ “{topic}”? Đây là 1 cách làm gọn mà hiệu quả.",
            "Đừng chạy theo 10 thứ — chỉ cần 1 điểm rơi để “{topic}” lên số.",
            "Nếu “{topic}” chưa ra đơn đều, có thể bạn thiếu 1 bước này.",
        ],
        "Process Optimization": [
            "Chỉ {t}s để gỡ rối “{topic}” bằng 1 workflow rõ ràng.",
            "Một mẹo nhỏ giúp “{topic}” chạy mượt hơn, ít lỗi hơn.",
            "Muốn “{topic}” nhanh hơn? Bắt đầu từ bước này.",
        ],
        "AI System": [
            "Nếu bạn muốn “{topic}” trông như một hệ thống, hãy bắt đầu từ kiến trúc.",
            "Đừng chỉ dùng tool — hãy biến “{topic}” thành pipeline có cấu trúc.",
            "Một cách đơn giản để “{topic}” có output ổn định hơn.",
        ],
        "Education": [
            "Học “{topic}” dễ hơn khi chia thành 3 bước nhỏ.",
            "Chỉ {t}s để hiểu “{topic}” theo cách rõ ràng, dễ nhớ.",
            "Một cách học “{topic}” không bị rối.",
        ],
        "General": [
            "Chỉ {t}s để hiểu điều quan trọng về “{topic}”.",
            "Một điều nhỏ xíu… nhưng có thể thay đổi cách bạn làm “{topic}”.",
            "Nếu “{topic}” khiến bạn rối, đây là 1 cách gỡ nhanh.",
        ],
    }
    hooks_en = {
        "Business Growth": [
            "Want better results from “{topic}”? Here’s a simple, high-leverage move.",
            "Stop doing 10 things—focus on the one conversion point for “{topic}”.",
            "If “{topic}” isn’t converting, you may be missing this step.",
        ],
        "Process Optimization": [
            "{t}s to unclog “{topic}” with a clean workflow.",
            "A small tweak to make “{topic}” smoother and less error-prone.",
            "To speed up “{topic}”, start here.",
        ],
        "AI System": [
            "To make “{topic}” a system, start with architecture.",
            "Don’t just use tools—turn “{topic}” into a structured pipeline.",
            "A simple way to get more consistent outputs for “{topic}”.",
        ],
        "Education": [
            "Learn “{topic}” faster by splitting it into 3 small steps.",
            "{t}s to understand “{topic}” clearly.",
            "A simple way to study “{topic}” without confusion.",
        ],
        "General": [
            "{t}s to understand what matters about “{topic}”.",
            "A tiny shift that changes how you handle “{topic}”.",
            "If “{topic}” feels messy, here’s a quick unlock.",
        ],
    }

    if language.lower().startswith("vi"):
        hook = _pick(hooks_vi[mode]).format(topic=topic, t=duration_sec)
        cta = "Nếu bạn muốn, mình có thể giúp bạn biến nó thành workflow chi tiết hơn."
    else:
        hook = _pick(hooks_en[mode]).format(topic=topic, t=duration_sec)
        cta = "If you want, I can help turn this into a more detailed workflow."

    # Mode-specific beats + script spine
    if mode == "Business Growth":
        beats = [
            "Nêu mục tiêu (đơn/CR/doanh thu) + bối cảnh",
            "Chỉ ra điểm nghẽn chuyển đổi",
            "Đưa 1 chiến lược trọng tâm (1 đòn bẩy)",
            "3 bước triển khai nhanh (hôm nay)",
            "Kết: KPI nhỏ để đo + khích lệ",
        ]
        script = f"""[{language.upper()} SCRIPT — ~{duration_sec}s | {platform}]
{hook}

(1) Mục tiêu: “{topic}” ra kết quả đều, không đốt sức.
(2) Điểm nghẽn hay gặp: bạn kéo traffic nhưng thiếu “điểm chốt”.
(3) Đòn bẩy: tối ưu 1 điểm — (Hook → Offer → Proof).
(4) Làm ngay 3 bước: viết 1 offer rõ, thêm 1 bằng chứng, và 1 CTA duy nhất.
(5) Đo bằng 1 KPI nhỏ (CR/đơn/ngày). {cta}
"""
        insight_visual = 'reveal a simple funnel concept (Hook→Offer→Proof) via icons/shapes, no readable text'
    elif mode == "Process Optimization":
        beats = [
            "Map quy trình hiện tại (rất ngắn)",
            "Xác định bottleneck (1 điểm)",
            "Đưa nguyên tắc tối ưu (Input→Process→Output)",
            "Tự động hoá 1 bước nhỏ",
            "Kết: checklist kiểm lỗi + khích lệ",
        ]
        script = f"""[{language.upper()} SCRIPT — ~{duration_sec}s | {platform}]
{hook}

(1) Với “{topic}”, mình luôn vẽ 1 dòng: Input → Process → Output.
(2) Bottleneck thường nằm ở 1 bước lặp lại nhiều nhất.
(3) Nguyên tắc: chuẩn hoá input trước, rồi mới tự động hoá process.
(4) Làm ngay: chọn 1 output, tạo 1 template input, rồi chạy batch.
(5) Thêm checklist kiểm lỗi 30 giây. {cta}
"""
        insight_visual = 'reveal a 3-step pipeline (Input→Process→Output) using shapes/icons, no readable text'
    elif mode == "AI System":
        beats = [
            "Nêu bài toán hệ thống",
            "Chọn output schema (đầu ra chuẩn)",
            "Module hoá workflow",
            "Test loop + logging",
            "Kết: API-ready + khích lệ",
        ]
        script = f"""[{language.upper()} SCRIPT — ~{duration_sec}s | {platform}]
{hook}

(1) Để “{topic}” thành hệ thống, bạn phải chốt đầu ra trước.
(2) Chọn 1 output schema: Outline/Script/Prompts (hoặc JSON).
(3) Module hoá: generator → validator → exporter.
(4) Chạy test loop: seed ổn định + log lỗi để sửa nhanh.
(5) Kiến trúc này cắm API sau rất dễ. {cta}
"""
        insight_visual = 'reveal modular blocks (generator→validator→exporter) as simple blocks/icons, no readable text'
    elif mode == "Education":
        beats = [
            "Mục tiêu học rõ ràng",
            "Tách 3 ý chính",
            "Ví dụ 1 tình huống",
            "Bài tập 10 phút",
            "Kết: khích lệ",
        ]
        script = f"""[{language.upper()} SCRIPT — ~{duration_sec}s | {platform}]
{hook}

(1) Với “{topic}”, mình chia thành 3 ý: Khái niệm – Ví dụ – Thực hành.
(2) Chỉ cần hiểu 1 câu định nghĩa và 1 ví dụ thật.
(3) Sau đó làm bài tập 10 phút: áp dụng vào 1 tình huống của bạn.
(4) Ghi lại 1 câu bạn học được hôm nay.
(5) Làm đều 7 ngày là thấy khác. {cta}
"""
        insight_visual = 'reveal a 3-part learning card (concept-example-practice) with icons, no readable text'
    else:
        beats = [
            "Mở cảnh gần gũi → nêu vấn đề",
            "Chỉ ra điểm nghẽn (1 câu)",
            "Bật mí nguyên tắc cốt lõi",
            "Hành động 1 bước (làm ngay)",
            "Kết: khích lệ + bước tiếp theo",
        ]
        script = f"""[{language.upper()} SCRIPT — ~{duration_sec}s | {platform}]
{hook}

(1) Mình bắt đầu với “{topic}” bằng cách bỏ bớt cái thừa.
(2) Điểm nghẽn thường là: làm quá nhiều thứ cùng lúc.
(3) Nguyên tắc: chia nhỏ thành 3 phần — Input → Process → Output.
(4) Bước làm ngay: chọn 1 output duy nhất, rồi quay ngược để biết cần input gì.
(5) {cta}
"""
        insight_visual = 'reveal a simple 3-step pipeline (Input→Process→Output) via shapes/icons, no readable text'

    outline = f"""MODE: {mode}
HOOK: {hook}

STRUCTURE (5 beats):
1) {beats[0]}
2) {beats[1]}
3) {beats[2]}
4) {beats[3]}
5) {beats[4]}

TARGET: {platform} | Duration: ~{duration_sec}s | Audience: {audience}
"""

    move1, move2, move3, move4, move5 = (_pick(camera_moves) for _ in range(5))

    shotlist = f"""SHOTLIST (5 shots)
S1 Hook: {move1} | close-up | prop: {_pick(props)} | metaphor: {_pick(metaphors)}
S2 Problem: {move2} | medium | show friction clearly (simple, non-violent)
S3 Insight: {move3} | insert | {insight_visual}
S4 Action: {move4} | hands-on | demonstrate the main step (clear and calm)
S5 Close: {move5} | wide | calm workspace, hopeful mood, subtle smile
"""

    prompts = f"""[PROMPT PACK — Offline draft, tool-ready]
GLOBAL LOOK:
- {style['global']}
- lighting: {style['lighting']}
- lens: {style['lens']}
- family-friendly, professional, no gore, no explicit content
- avoid readable text artifacts, avoid watermark artifacts
- consistent style across shots

SCENE CONTEXT:
- Topic: "{topic}"
- Mode: {mode}
- Platform: {platform} | Duration: ~{duration_sec}s | Audience: {audience}

SHOT 1 (Hook):
{style['global']}, {style['lighting']}, {move1}, close-up, {_pick(props)}, expressive but subtle, clean background

SHOT 2 (Problem):
{style['global']}, {style['lighting']}, {move2}, medium shot, show the friction/bottleneck visually, clear storytelling

SHOT 3 (Insight):
{style['global']}, {style['lighting']}, {move3}, insert shot, {insight_visual}

SHOT 4 (Action):
{style['global']}, {style['lighting']}, {move4}, hands arranging steps, one clear action, confident pacing

SHOT 5 (Close):
{style['global']}, {style['lighting']}, {move5}, wide shot, calm workspace, warm hopeful mood, gentle smile
"""

    meta = {
        "generated_at": _now_stamp(),
        "mode": "offline_mock_adaptive",
        "detected_mode": mode,
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
        mode=mode,
        outline=outline,
        script=script,
        shotlist=shotlist,
        prompts=prompts,
        meta=meta,
    )

def build_markdown(res: WorkflowResult) -> str:
    return f"""# GlowMiniAI Output Pack
Topic: {res.topic}
Mode: {res.mode}
Language: {res.language}
Platform: {res.platform}
Duration: {res.duration_sec}s
Audience: {res.audience}
Style: {res.style_preset}
Generated: {res.meta.get('generated_at')}
Engine: {res.meta.get('mode')}

## Outline
{res.outline}

## Script
{res.script}

## Shotlist
{res.shotlist}

## Prompt Pack
{res.prompts}

## Meta
{json.dumps(res.meta, ensure_ascii=False, indent=2)}
"""

def save_pack(res: WorkflowResult, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    stamp = res.meta.get("generated_at") or _now_stamp()
    fname = f"{stamp}_{_safe_name(res.topic)}.md"
    path = os.path.join(out_dir, fname)
    content = build_markdown(res)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
