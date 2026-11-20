"""
vr_config.py: shared settings for all Python services in this repo.

Every machine-specific value is read from an environment variable, with a
default that works on a fresh clone. Set these before starting the services
(see README.md, "Configuration").

  UNITY_PROJECT_DIR  Root folder of your Unity project. room_config.json is
                     written here and generated scripts are copied to its
                     Assets folder. Default: ./unity_project (inside this repo)
  AI_OUTPUT_DIR      Folder for generated images (wall textures, NPC portraits,
                     door and picture PNGs). The Unity scripts read the same
                     variable. Default: <UNITY_PROJECT_DIR>/ai_output
  OLLAMA_URL         Ollama generate endpoint. Default: http://localhost:11434/api/generate
  OLLAMA_MODEL       Ollama model name. Default: llama3.2:3b
  VR_BIND_HOST       Network interface for the web and voice servers.
                     Default: 127.0.0.1 (this computer only).
                     Use 0.0.0.0 only if a headset on your network must reach them.
"""

import os
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent

UNITY_PROJECT_DIR = Path(
    os.environ.get("UNITY_PROJECT_DIR", REPO_DIR / "unity_project")
).expanduser()
UNITY_ASSETS = UNITY_PROJECT_DIR / "Assets"

AI_OUTPUT_DIR = Path(
    os.environ.get("AI_OUTPUT_DIR", UNITY_PROJECT_DIR / "ai_output")
).expanduser()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

BIND_HOST = os.environ.get("VR_BIND_HOST", "127.0.0.1")
