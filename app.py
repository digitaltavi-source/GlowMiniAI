import streamlit as st
from workflows.engine import generate_media_pack, save_pack, build_markdown, quality_check_pack

# Optional Gemini backend (will only be used if installed + API key provided)
try:
    from workflows.gemini_llm import gemini_generate_pack
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False


st.set_page_config(page_title="GlowMiniAI (Offline + Gemini)", page_icon="✨", layout="centered")

# Optional logo (won't break if missing)
try:
    st.image("assets/glow_logo_hd.png", width=110)
except Exception:
    pass

st.markdown("# ✨ GlowMiniAI — Portable AI Workflow Engine")
st.caption("Chạy offline không cần API key. Nếu có Gemini API key → nội dung sẽ sâu & đa dạng hơn.")

st.info("Architecture: UI (Streamlit) → Workflow Engine → (Offline Mock | Gemini LLM) → QC → Export/Download (.md)")

# ===== Engine Mode =====
engine_options = ["Offline (Mock)"]
if GEMINI_AVAILABLE:
    engine_options.append("Gemini (API)")
engine_mode = st.selectbox("Engine", engine_options, index=0)

api_key = ""
if engine_mode == "Gemini (API)":
    api_key = st.text_input("Gemini API Key", type="password", help="Không có key → hãy chọn Offline. Key chỉ dùng trên máy bạn khi nhập vào.")
    if not api_key.strip():
        st.warning("Chưa có API key. Hãy dán key hoặc chuyển về Offline (Mock).")

# ===== Inputs =====
topic = st.text_input("Chủ đề / Topic", value="Tối ưu quy trình tạo nội dung cho shop online")

colA, colB = st.columns(2)
with colA:
    lang = st.selectbox("Ngôn ngữ", ["vi", "en"], index=0)
with colB:
    platform = st.selectbox("Nền tảng", ["YouTube Shorts", "TikTok", "Facebook Reels", "Website/Blog"], index=0)

colC, colD = st.columns(2)
with colC:
    duration = st.slider("Thời lượng (giây)", 15, 60, 35, 5)
with colD:
    audience = st.selectbox("Đối tượng", ["General", "Kids/Family", "Business", "Education"], index=0)

style_preset = st.selectbox("Style preset", ["Cinematic 3D", "Clean Minimal", "Handcrafted Cozy", "Tech Explainer"], index=0)

seed_toggle = st.checkbox("Giữ kết quả ổn định (seed) — chỉ áp dụng Offline", value=True)
seed = st.number_input("Seed", 0, 999999, 42, 1) if seed_toggle else None

out_dir = st.text_input("Local output folder (chỉ dùng khi chạy local)", value="output")

col1, col2, col3 = st.columns(3)
with col1:
    gen = st.button("Generate", use_container_width=True)
with col2:
    save_local = st.button("Save to /output (local)", use_container_width=True)
with col3:
    download = st.button("Download .md", use_container_width=True)

# ===== Run =====
if gen or save_local or download:
    if not topic.strip():
        st.error("Vui lòng nhập chủ đề.")
    else:
        # ---------- Generate with Gemini if selected and key provided ----------
        used_engine = "Offline"
        mode = ""
        outline = ""
        script = ""
        shotlist = ""
        prompts = ""

        if engine_mode == "Gemini (API)" and api_key.strip():
            try:
                data = gemini_generate_pack(
                    api_key=api_key.strip(),
                    topic=topic.strip(),
                    language=lang,
                    platform=platform,
                    duration_sec=int(duration),
                    audience=audience,
                    style_preset=style_preset,
                )
                used_engine = "Gemini"
                mode = data.get("mode", "LLM")
                outline = data.get("outline", "")
                script = data.get("script", "")
                shotlist = data.get("shotlist", "")
                prompts = data.get("prompts", "")
                st.success(f"✅ Generated with **Gemini**. Mode: **{mode}**")
            except Exception as e:
                st.error(f"Gemini error → fallback Offline. Details: {e}")

        # ---------- Offline fallback ----------
        if used_engine != "Gemini":
            res = generate_media_pack(
                topic=topic.strip(),
                language=lang,
                platform=platform,
                duration_sec=int(duration),
                audience=audience,
                style_preset=style_preset,
                seed=int(seed) if seed is not None else None,
            )
            used_engine = "Offline"
            mode = res.mode
            outline = res.outline
            script = res.script
            shotlist = res.shotlist
            prompts = res.prompts
            st.success(f"✅ Generated with **Offline**. Detected Mode: **{mode}**")

        # ---------- Display ----------
        st.subheader("Outline")
        st.code(outline)

        st.subheader("Script")
        st.code(script)

        st.subheader("Shotlist")
        st.code(shotlist)

        st.subheader("Prompt Pack")
        st.code(prompts)

        # ---------- QC ----------
        st.subheader("🔍 Quality Control")
        scores, avg_score, suggestions = quality_check_pack(outline, script, shotlist, prompts)

        st.write(f"**Average Score:** {avg_score}/10")
        for k, v in scores.items():
            st.write(f"- {k}: {v}/10")

        if suggestions:
            st.write("**Suggestions:**")
            for s in suggestions:
                st.write(f"- {s}")
        else:
            st.success("Output quality is strong. No major issues detected.")

        # ---------- Markdown pack ----------
        md = f"""# GlowMiniAI Output Pack
Topic: {topic.strip()}
Engine: {used_engine}
Mode: {mode}
Language: {lang}
Platform: {platform}
Duration: {int(duration)}s
Audience: {audience}
Style: {style_preset}

## Outline
{outline}

## Script
{script}

## Shotlist
{shotlist}

## Prompt Pack
{prompts}
"""

        # Local save (only meaningful on local)
        if save_local:
            # If offline, you can save using existing helper; if Gemini, save the assembled md
            if used_engine == "Offline":
                path = save_pack(res, out_dir)  # type: ignore
                st.info(f"📄 Saved locally: {path}")
            else:
                import os, datetime
                os.makedirs(out_dir, exist_ok=True)
                fname = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{topic.strip().replace(' ', '_')[:40]}.md"
                path = os.path.join(out_dir, fname)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(md)
                st.info(f"📄 Saved locally: {path}")

        # Download
        if download:
            filename = f"GlowMiniAI_{used_engine}_{mode}_{topic.strip()}".replace(" ", "_")[:90] + ".md"
            st.download_button(
                label="⬇️ Click to download .md",
                data=md,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )

st.markdown("---")
st.markdown("### Run locally")
st.code(
    "python -m pip install -r requirements.txt\n"
    "python -m streamlit run app.py\n\n"
    "# Launcher:\n"
    "SETUP_AND_RUN.bat\n",
    language="bash",
)

st.caption("GlowMiniAI | Offline Mock + Optional Gemini API | QC + Download-ready | Python + Streamlit")
