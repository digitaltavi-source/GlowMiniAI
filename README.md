# GlowMiniAI (Portable Offline Demo)

A tiny, **offline** AI workflow demo kit that runs **without any API key**.

## What it does
Generates a simple pack:
- Outline
- Short script
- Prompt pack (global + per-shot)

## Run (UI)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run (CLI)
```bash
python glowctl.py "Tối ưu hóa quy trình" --lang vi
```

Outputs are saved to the `output/` folder as `.md`.

## Notes
This kit uses an **offline mock generator** (template + structured randomness).
Later, you can plug in an LLM provider while keeping the same output schema.
