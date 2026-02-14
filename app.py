import streamlit as st
from workflows.engine import generate_media_pack, save_pack, build_markdown, quality_check_pack

st.set_page_config(page_title="GlowMiniAI (Offline Build)", page_icon="✨", layout="centered")

# Optional logo (won't break if missing)
try:
    st.image("assets/glow_logo_hd.png", width=110)
except Exception:
    pass

st.markdown("# ✨ GlowMiniAI — Portable AI Workflow Engine (Offline Build)")
st.caption("Chạy được ngay **không cần API key**. Output: Outline • Script • Shotlist • Prompt Pack.")

st.info("Architecture: UI (Streamlit) → Workflow Engine → Offline Generation Layer → Export (.md) → (Future API)")
st.markdown("**Mode:** Adaptive offline mock (topic-based routing) | **Goal:** stable, usable outputs for demo & production drafts.")

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

seed_toggle = st.checkbox("Giữ kết quả ổn định (seed)", value=True)
seed = st.number_input("Seed", 0, 999999, 42, 1) if seed_toggle else None

out_dir = st.text_input("Local output folder (chỉ dùng khi chạy local)", value="output")

col1, col2, col3 = st.columns(3)
with col1:
    gen = st.button("Generate", use_container_width=True)
with col2:
    save_local = st.button("Save to /output (local)", use_container_width=True)
with col3:
    download = st.button("Download .md", use_container_width=True)

if gen or save_local or download:
    if not topic.strip():
        st.error("Vui lòng nhập chủ đề.")
    else:
        res = generate_media_pack(
            topic=topic.strip(),
            language=lang,
            platform=platform,
            duration_sec=int(duration),
            audience=audience,
            style_preset=style_preset,
            seed=int(seed) if seed is not None else None,
        )

        st.success(f"✅ Generated. Detected Mode: **{res.mode}**")

        st.subheader("Outline")
        st.code(res.outline)

        st.subheader("Script")
        st.code(res.script)

        st.subheader("Shotlist")
        st.code(res.shotlist)

        st.subheader("Prompt Pack")
        st.code(res.prompts)

        # ✅ QC must be inside this block (after we have res)
        st.subheader("🔍 Quality Control")
        scores, avg_score, suggestions = quality_check_pack(res.outline, res.script, res.shotlist, res.prompts)

        st.write(f"**Average Score:** {avg_score}/10")
        for k, v in scores.items():
            st.write(f"- {k}: {v}/10")

        if suggestions:
            st.write("**Suggestions:**")
            for s in suggestions:
                st.write(f"- {s}")
        else:
            st.success("Output quality is strong. No major issues detected.")

        md = build_markdown(res)

        if save_local:
            path = save_pack(res, out_dir)
            st.info(f"📄 Saved locally: {path}")

        if download:
            filename = f"GlowMiniAI_{res.mode}_{res.topic}".replace(" ", "_")[:80] + ".md"
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
    "SETUP_AND_RUN.bat\n\n"
    "# CLI:\n"
    "python glowctl.py \"chu de cua ban\" --lang vi",
    language="bash",
)

st.markdown("---")
st.caption("GlowMiniAI | Adaptive Offline Mock Engine | QC + Download-ready | Python + Streamlit")
