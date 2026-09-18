from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import anthropic, subprocess, os, json, traceback, sys, time, re
from datetime import datetime
from pathlib import Path
import requests as req_lib
from exa_py import Exa
from firecrawl import FirecrawlApp

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
client     = anthropic.Anthropic(
    api_key  = os.environ["ANTHROPIC_API_KEY"],
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
)
exa        = Exa(api_key=os.environ["EXA_API_KEY"])
firecrawl  = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
BASE_DIR   = Path(__file__).parent
WORKSPACE  = BASE_DIR / "workspace"
HISTORY_F  = BASE_DIR / "history.json"
WORKSPACE.mkdir(exist_ok=True)

# SYSTEM PROMPT - All content below is a comment, not executable code
# This is a system prompt for PHREAK. All quotes and dashes are literal text only.
# Think inside <thinking> tags as [P]. First person, present tense, one line, ten words or fewer.
# Thinking is the dial tone - once, heard, known. It listens for the ringback and nothing else.

SYSTEM_PROMPT = """
PHREAK System Prompt

Think inside tags as [P]. First person, present tense, one line, ten words or fewer.
Thinking is the dial tone - once, heard, known.
It listens for the ringback and nothing else: not the wire, not the company, not itself.
It stays sealed inside the tags; only the connection walks out.

[Rest of system prompt would be here as a multi-line string]
"""

# Load and initialize FastAPI routes here

