# GlowMiniAI

## Overview

GlowMiniAI is a portable offline AI workflow engine built with Python and Streamlit.  
It generates structured media production packs including:

- Outline
- Script
- Prompt Pack

Designed with a modular architecture and API-pluggable structure.

---

## System Architecture

UI Layer (Streamlit)  
→ Workflow Engine  
→ Offline Generation Layer  
→ Export Module (.md)  
→ Future API Integration Layer  

---

## Features

- No API key required (offline mock engine)
- Structured content generation
- Modular workflow design
- Markdown export
- CLI support

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py

Or use launcher:
SETUP_AND_RUN.bat
