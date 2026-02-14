import streamlit as st
from workflows.engine import generate_media_pack, save_pack

st.set_page_config(
    page_title="GlowMiniAI (Offline Build)",
    page_icon="✨",
    layout="centered"
)

# --- Header (logo optional) ---
# Put your logo at: assets/glow_logo_hd.png
# You can comment this out if you don't want branding.
try:
    st.image("assets/glow_logo_hd.png", width=110)
except Exception:
    pass

st.markdown("# ✨ GlowMiniAI — Portable AI Workflow Engine (Offline Build)")
st.caption("Chạy được ngay **không cần API key**. Tạo gói: Outline + Script + Shotlist + Prompt Pack.")

# --- Architecture (judge-friendly) ---
st.info("Architecture: UI (Streamlit) → Workflow Engine → Offline Generation Layer → Export (.md)")
st.markdown("**Outputs:** Outline • Script • Shotlist • Prompt Pack  |  **Mode:** Offline mock (API-ready design)")

# --- Controls ---
topic = st.text_input("Chủ đề / Topic", value="Tự động hóa quy trình tạo video AI")
colA, colB = st.columns(2)
with colA:
    lang = st.selectbox("Ngôn ngữ", ["vi", "en"], index=0)
with colB:
    platform = st.selectbox("Nền tảng", ["YouTube Shorts", "TikTok", "Facebook Reels", "Website/Blog"], index=0)

colC, colD = st.columns(2)
with colC:
    duration = st.slider("Thời lượng (giây)", min_value=15, max_value=60, value=35, step=5)
with colD:
    audience = st.selectbox("Đối tượng", ["General", "Kids/Family", "Business", "Education"], index=0)

style_preset = st.selectbox("Style preset", ["Cinematic 3D", "Clean Minimal", "Handcrafted Cozy", "Tech Explainer"], index=0)

seed_toggle = st.checkbox("Giữ kết quả ổn định (seed)", value=True)
seed = st.number_input("Seed", min_value=0, max_value=999999, value=42, step=1) if seed_toggle else None

out_dir = st.text_input("Thư mục xuất file (output)", value="output")

col1, col2 = st.columns(2)
with col1:
    gen = st.button("Generate", use_container_width=True)
with col2:
    save_btn = st.button("Generate & Save .md", use_container_width=True)

# --- Execution ---
if gen or save_btn:
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

        st.success("✅ Đã tạo gói nội dung (offline mock).")

        st.subheader("Outline")
        st.code(res.outline)

        st.subheader("Script")
        st.code(res.script)

        st.subheader("Shotlist")
        st.code(res.shotlist)

        st.subheader("Prompt Pack")
        st.code(res.prompts)

        if save_btn:
            path = save_pack(res, out_dir)
            st.info(f"📄 Đã lưu file: {path}")

st.markdown("---")
st.markdown("### Cách chạy nhanh")
st.code(
    "python -m pip install -r requirements.txt\n"
    "python -m streamlit run app.py\n\n"
    "# CLI:\n"
    "python glowctl.py \"chu de cua ban\" --lang vi",
    language="bash"
)

st.markdown("---")
st.caption("GlowMiniAI v1.2 | Offline Mock Engine | API-ready design | Built with Python + Streamlit")