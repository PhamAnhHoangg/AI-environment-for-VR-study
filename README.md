# AI Environment for VR Study: German Medical VR

[![checks](https://github.com/PhamAnhHoangg/AI-environment-for-VR-study/actions/workflows/ci.yml/badge.svg)](https://github.com/PhamAnhHoangg/AI-environment-for-VR-study/actions/workflows/ci.yml)

A VR environment for learning medical German. A Python backend with a local LLM (Ollama), speech recognition (Whisper) and a text-to-speech doctor drives a Unity 6 scene: you talk to an NPC doctor, quiz yourself on objects in the room, and use the Builder mode to have an AI generate new room variations.

This repository holds the Python services, the Unity C# scripts and the helper scripts. It does **not** contain the Unity project itself (scenes, `ProjectSettings/`, `Packages/`). See [Unity side](#unity-side).

Project report and slides: [`docs/`](docs/).

## What is in it

| Part | What it does | Files |
|------|--------------|-------|
| Web app (port 7863) | Learner mode: two fixed rooms with a bilingual NPC chat. Builder mode: AI generates a variation of the Doctor or Reception room and writes `room_config.json` | `gradio_app_v2.py` |
| Room AI generator (port 7865) | Asks an LLM to write room C# scripts and deploys them to the Unity project | `room_ai_gradio.py`, `room_ai_generator.py` |
| Speech to text (port 7864) | Whisper transcription of the learner's microphone audio | `whisper_server.py` |
| Text to speech (port 7866) | German and English doctor voice (edge-tts, offline fallback pyttsx3) | `tts_server.py` |
| LLM (port 11434) | Local Ollama server, default model `llama3.2:3b` | external, [ollama.com](https://ollama.com) |
| Unity scripts | Room building, NPC chat UI, voice recorder, quizzes, config hot-reload | `*.cs`, `Editor/` |
| Image tools (optional) | Quiz images, NPC sprites, room presets | `generate_*.py`, `pixelize_npc.py` |

## Quick start (Windows)

1. Clone the repo and open a terminal in its folder.
2. Right-click `setup.bat` and run it as administrator. It installs Git, Python 3.10, Unity Hub, Unity 6000.4.3f1 and the packages in `requirements.txt`. The first run takes 15 to 30 minutes.
3. Install [Ollama](https://ollama.com), then pull the model: `ollama pull llama3.2:3b`
4. Run `START_ALL.bat`. It starts Ollama, Whisper, the web app, the Room AI generator and the TTS server in separate windows.
5. Open http://localhost:7863. Run `STOP_ALL.bat` to stop everything.

Optional features (image generation, pixel-art sprites, random colour palettes, offline voice): `pip install -r requirements-optional.txt`

## Unity side

The Python services and the Unity project live in two places on your machine. The Python code writes `room_config.json` and generated scripts into your Unity project, and the Unity scripts read them.

1. Create or open your Unity 6000.4.3f1 project in Unity Hub.
2. Set `UNITY_PROJECT_DIR` to that project's root folder (see below), then open a new terminal.
3. Run `sync_to_unity.bat` to copy the C# scripts from this repo into `<UNITY_PROJECT_DIR>\Assets`. Run `setup_varjo.ps1` to add the Varjo and OpenXR packages to the project manifest.
4. Press Play. The scripts hot-reload `room_config.json` whenever the web app saves it.

`deploy_vr.bat` builds the app and installs it on a Meta Quest over ADB. Edit the paths at the top of the script if Unity or ADB are installed elsewhere.

## Configuration

Everything machine-specific is an environment variable. Set one permanently with `setx NAME "value"` and open a new terminal.

| Variable | Default | Purpose |
|----------|---------|---------|
| `UNITY_PROJECT_DIR` | `./unity_project` | Unity project root. `room_config.json` is written here and generated scripts go to its `Assets` folder |
| `AI_OUTPUT_DIR` | `<UNITY_PROJECT_DIR>/ai_output` | Folder for generated images. The Unity scripts read the same variable, so set it before starting Unity Hub |
| `OLLAMA_MODEL` | `llama3.2:3b` | Ollama model used by the chat and the builder |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama endpoint |
| `VR_BIND_HOST` | `127.0.0.1` | Network interface of the web and voice servers. Use `0.0.0.0` (or `set VR_LAN=1` before `START_ALL.bat`) only if a headset on your network must reach them |
| `VR_PYTHON` | `python` | Interpreter used by `START_ALL.bat` |
| `GROQ_API_KEY`, `GEMINI_API_KEY` | empty | Optional cloud LLMs for the Room AI generator. Never commit keys |

## Ports

| Port | Service |
|------|---------|
| 7863 | Web app (Learner and Builder) |
| 7864 | Whisper speech to text |
| 7865 | Room AI generator |
| 7866 | Doctor text to speech |
| 11434 | Ollama |

## Requirements

| Tool | Version |
|------|---------|
| Windows | 10 or 11 (the helper scripts are Windows only) |
| Unity | 6000.4.3f1 with Android module for Quest builds |
| Python | 3.10 or newer |
| Ollama | latest |
| CUDA (optional) | 11.8 or newer for GPU Whisper |
| Varjo Base (optional) | 4.16 or newer, about 4 GB free on C: |

## Troubleshooting

- **`ModuleNotFoundError`**: run `pip install -r requirements.txt`, and `pip install -r requirements-optional.txt` for the optional tools.
- **Chat says Ollama is not running or the model is missing**: run `ollama serve`, then `ollama pull llama3.2:3b`.
- **Unity cannot find the Android SDK**: in Unity Hub open Installs, your version, Add Modules, Android.
- **Whisper is slow**: install PyTorch with CUDA: `pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118`
- **Unity does not find generated images**: make sure Unity and the Python tools use the same `AI_OUTPUT_DIR`. Unity only sees variables that were set before Unity Hub started.

## Checks

GitHub Actions runs on every push and pull request: all Python files must compile, `ruff` looks for real errors (syntax, undefined names, unused variables), and `tests/test_basics.py` checks `room_config.json` (colours, German nouns with their article), the room colour rules (walls and ceiling the same bright colour) and the settings in `vr_config.py`. The heavy AI packages and the Unity C# code are not run there. Run the tests yourself with:

```
python -m unittest discover -s tests -v
```

## Repository layout

```
.
├── gradio_app_v2.py         Web app (Learner + Builder)
├── room_ai_gradio.py        Room AI generator UI
├── room_ai_generator.py     LLM prompts and script deployment
├── whisper_server.py        Speech to text API
├── tts_server.py            Text to speech API
├── vr_config.py             Paths, model and host settings (environment variables)
├── color_fetcher.py         Random room colour palettes
├── generate_*.py            Quiz images, NPC sprites, room presets
├── *.cs, Editor/            Unity scripts (copied into the Unity project)
├── room_config.json         Example room configuration
├── quiz_images/             Quiz pictures
├── docs/                    Project report and slides
├── START_ALL.bat            Start every service
├── STOP_ALL.bat             Stop every service
├── setup.bat                Install prerequisites
├── sync_to_unity.bat        Copy C# scripts into the Unity project
├── deploy_vr.bat            Build and install on a Meta Quest
└── requirements*.txt        Python dependencies
```

## License

MIT, see [LICENSE](LICENSE). The Unity project itself, third-party packages and the Ollama and Whisper models are not part of this repository and have their own licenses.
