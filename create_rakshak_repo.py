#!/usr/bin/env python3
"""
create_rakshak_repo.py
Creates a ready-to-edit scaffold for the Rakshak AI Kaggle submission.
Run: python create_rakshak_repo.py
"""

import os
from pathlib import Path
import json
import textwrap

ROOT = Path.cwd() / "rakshak-ai"

def write(path: Path, content: str, mode='w'):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f"Created {path.relative_to(ROOT.parent)}")

# 1. Repo layout and simple files
files = {
    "README.md": f"""# RAKSHAK AI — Multi-Agent Accident Prevention & Safe Mobility

**Track:** Agents for Good  
**Authors:** Sweymaan & Team Vijay  
**Submission:** Kaggle Agents Intensive Capstone (Dec 1, 2025)

---

## One-line pitch
RAKSHAK AI is a multi-agent safety co-pilot that predicts accident risk in real-time, detects dangerous driver states, monitors vehicle health, and shares precise V2V alerts — powered by Gemini Vision + ADK-style agents.

---

## What this repo contains
- `kaggle_notebook.ipynb` — demo notebook (placeholder)
- `src/` — agent and tool skeletons (vision, risk, guardian, etc.)
- `examples/run_demo.py` — a simple offline demo script
- `docs/` — architecture diagram, deployment and evaluation docs
- `data/` — sample frames and OBD example (add your own images here)

---

## How to run (local demo)
1. (Optional) Create a virtual environment: `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python examples/run_demo.py`

**Important:** This repository contains *mock/demo* code. Replace Gemini API calls with your credentials or mocks. **Do not** commit API keys.

""",
    "LICENSE": "MIT License\n\nCopyright (c) 2025 Sweymaan",
    "CODE_OF_CONDUCT.md": "# Code of Conduct\nBe kind and respectful.",
    ".gitignore": "venv/\n__pycache__/\n*.pyc\n.DS_Store\ndata/sample_frames/*\n.env\n",
    "requirements.txt": "\n".join([
        "numpy",
        "scikit-learn",
        "matplotlib",
        "pillow",
        "opencv-python",
        "notebook",
    ]),
    ".github/workflows/ci.yml": textwrap.dedent("""\
        name: CI

        on:
          push:
            branches: [ main ]
          pull_request:
            branches: [ main ]

        jobs:
          test:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v3
              - name: Set up Python
                uses: actions/setup-python@v4
                with:
                  python-version: '3.10'
              - name: Install deps
                run: |
                  python -m pip install --upgrade pip
                  pip install -r requirements.txt
              - name: Run demo script
                run: python examples/run_demo.py
    """),
    "kaggle_notebook.ipynb": json.dumps({
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": ["# RAKSHAK AI — Demo Notebook\n\nThis notebook runs a small offline demo of the multi-agent system (mocked Gemini responses)."]},
        ],
        "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3"}, "language_info": {"name": "python"}},
        "nbformat": 4,
        "nbformat_minor": 5
    }, indent=2),
    "demo_video_script.txt": textwrap.dedent("""\
        RAKSHAK AI — 3-minute demo script

        0:00-0:20 - Problem: Road safety & motivation (facts)
        0:20-0:40 - Why agents: multi-sensor & continuous monitoring
        0:40-1:10 - Architecture overview (screen showing diagram)
        1:10-2:10 - Demo: run notebook; show vision detection -> risk score -> alert
        2:10-2:40 - Results & evaluation slides (charts)
        2:40-3:00 - Next steps and closing
    """),
    "docs/architecture.txt": "See docs/architecture.png (drawn from notebook).",
    "docs/deployment.md": textwrap.dedent("""\
        Deployment notes (summary)
        - This repo is demo-first. To deploy:
          1. Replace Gemini/mock calls with real API usage (store keys in env).
          2. Containerize core agents (Dockerfile) and push to GCR.
          3. Use Vertex AI Agent Engine or Cloud Run to host the orchestration service.
    """),
    "docs/evaluation.md": textwrap.dedent("""\
        Evaluation plan:
        - Vision Agent: precision/recall on drowsiness dataset (small hand-labeled set).
        - Risk Model: ROC AUC vs baseline (speed threshold).
        - Safety value: estimated time saved by rerouting (synthetic).
    """),
}

# 2. Source skeletons
agents = {
    "src/agents/assistant_agent.py": textwrap.dedent("""\
        # Assistant Agent - routes user requests to sub-agents (skeleton)
        class AssistantAgent:
            def __init__(self, vision, risk, guardian, memory):
                self.vision = vision
                self.risk = risk
                self.guardian = guardian
                self.memory = memory

            def handle_frame(self, frame_path, obd_sample=None, context=None):
                obs = self.vision.analyze_frame(frame_path)
                score = self.risk.compute_risk(obs, context)
                alert = self.guardian.maybe_alert(score, obs, context)
                return {'obs': obs, 'score': score, 'alert': alert}
    """),
    "src/agents/vision_agent.py": textwrap.dedent("""\
        # Vision Agent (Gemini Vision + YOLO skeleton)
        from typing import Dict, Any
        from src.utils.observability import logger

        class VisionAgent:
            def __init__(self, gemini_client=None, yolo_model=None):
                self.gemini = gemini_client
                self.yolo = yolo_model

            def analyze_frame(self, frame_path: str) -> Dict[str, Any]:
                # In demo we mock outputs. Replace with actual YOLO + Gemini Vision calls.
                yolo_res = {'labels': ['person', 'phone'], 'boxes': []}
                gemini_res = {'drowsy_score': 0.8, 'face_confidence': 0.95}
                obs = {
                    'yolo': yolo_res,
                    'gemini': gemini_res,
                    'drowsy_score': gemini_res.get('drowsy_score', 0.0),
                    'phone_detected': 'phone' in yolo_res.get('labels', [])
                }
                logger.info("VisionAgent -> obs: %s", obs)
                return obs
    """),
    "src/agents/driver_state_agent.py": textwrap.dedent("""\
        # Driver State Agent - fuses vision + OBD (skeleton)
        class DriverStateAgent:
            def __init__(self):
                pass

            def classify(self, obs, obd):
                # simple heuristic
                dscore = obs.get('drowsy_score', 0.0)
                phone = obs.get('phone_detected', False)
                if dscore > 0.7:
                    return 'Drowsy'
                if phone:
                    return 'Distracted'
                return 'Alert'
    """),
    "src/agents/risk_agent.py": textwrap.dedent("""\
        # Risk Agent - uses a model to compute risk score (skeleton)
        from src.utils.observability import logger

        class RiskAgent:
            def __init__(self, model=None, risk_tool=None):
                self.model = model
                self.risk_tool = risk_tool

            def compute_risk(self, obs, context) -> float:
                # Demo: compute a combined heuristic score
                base = obs.get('drowsy_score', 0.0) * 0.6
                phone = 0.2 if obs.get('phone_detected') else 0.0
                weather = context.get('weather_risk', 0.0) if context else 0.0
                score = min(100, (base + phone + weather) * 100)
                logger.info("RiskAgent -> score: %.2f", score)
                return score
    """),
    "src/agents/vehicle_health_agent.py": textwrap.dedent("""\
        # Vehicle Health Agent (skeleton)
        class VehicleHealthAgent:
            def __init__(self):
                pass

            def analyze_obd(self, obd):
                # Simple anomaly heuristics
                issues = []
                if obd.get('tire_pressure', 32) < 28:
                    issues.append('low_tire_pressure')
                return {'issues': issues}
    """),
    "src/agents/v2v_agent.py": textwrap.dedent("""\
        # V2V Agent (simulated broadcast)
        def broadcast_v2v(message, location):
            # In a real system use DSRC/5G; here we print/log for demo
            print('[V2V BROADCAST]', message, location)
    """),
    "src/agents/guardian_agent.py": textwrap.dedent("""\
        # Guardian Agent - long-running monitoring & alerts
        from src.memory.memory_bank import MemoryBank
        from src.tools.alert_tool import push_alert

        class GuardianAgent:
            def __init__(self, memory_path='data/memory.json'):
                self.memory = MemoryBank(path=memory_path)

            def maybe_alert(self, score, obs, context):
                level = 0
                if score > 95:
                    level = 3
                elif score > 80:
                    level = 2
                elif score > 50:
                    level = 1
                if level > 0:
                    msg = f'Risk {score:.1f}% detected'
                    push_alert(level, msg, context.get('location', {}))
                    self.memory.add_hotspot(context.get('location', {}), score)
                    return {'level': level, 'message': msg}
                return None
    """),
}

tools = {
    "src/tools/camera_tool.py": textwrap.dedent("""\
        # Camera tool (stub)
        def read_frame(path):
            with open(path, 'rb') as f:
                return f.read()
    """),
    "src/tools/risk_tool.py": textwrap.dedent("""\
        # Risk tool (stub)
        def extract_features(obs, context):
            return {
                'drowsy': obs.get('drowsy_score', 0.0),
                'phone': 1 if obs.get('phone_detected') else 0,
                'weather': context.get('weather_risk', 0.0) if context else 0.0
            }
    """),
    "src/tools/obd_tool.py": textwrap.dedent("""\
        # OBD tool (stub)
        def parse_obd(obd_json):
            return obd_json
    """),
    "src/tools/alert_tool.py": textwrap.dedent("""\
        # Alert tool (stub)
        def push_alert(level:int, message:str, location:dict):
            print(f"[ALERT {level}] {message} @ {location}")
    """),
}

memory = {
    "src/memory/memory_bank.py": textwrap.dedent("""\
        import json, time
        class MemoryBank:
            def __init__(self, path='data/memory.json'):
                self.path = path
                try:
                    with open(self.path) as f:
                        self.store = json.load(f)
                except:
                    self.store = {'hotspots': [], 'trips': []}

            def add_hotspot(self, geo, score):
                self.store.setdefault('hotspots', []).append({'geo':geo, 'score':score, 'ts': time.time()})
                self._flush()

            def add_trip(self, trip):
                self.store.setdefault('trips', []).append(trip)
                self._flush()

            def _flush(self):
                with open(self.path,'w') as f:
                    json.dump(self.store, f, indent=2)
    """),
}

sessions = {
    "src/sessions/in_memory_session.py": textwrap.dedent("""\
        # Simple in-memory session service (demo)
        class InMemorySessionService:
            def __init__(self):
                self.sessions = {}

            def create(self, session_id, data):
                self.sessions[session_id] = data

            def get(self, session_id):
                return self.sessions.get(session_id, {})
    """),
}

utils = {
    "src/utils/observability.py": textwrap.dedent("""\
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('rakshak')
    """),
    "src/utils/metrics.py": textwrap.dedent("""\
        # Simple metrics counters
        metrics = {'alerts': 0, 'high_risk': 0}
        def inc(metric):
            metrics[metric] = metrics.get(metric,0) + 1
    """),
}

models = {
    "src/models/accident_model.py": textwrap.dedent("""\
        # Accident model placeholder
        def load_demo_model():
            # Return a simple mock model with predict_proba
            class MockModel:
                def predict_proba(self, X):
                    # return probabilities [[0.2, 0.8]] style
                    return [[0.3, 0.7] for _ in X]
            return MockModel()
    """),
    "src/models/evaluation.py": textwrap.dedent("""\
        # Evaluation helpers (demo)
        def evaluate_predictions(y_true, y_pred):
            # simple accuracy
            correct = sum(1 for a,b in zip(y_true,y_pred) if a==b)
            return correct/len(y_true)
    """),
}

examples = {
    "examples/run_demo.py": textwrap.dedent("""\
        # Simple demo runner that wires skeleton agents together
        from src.agents.vision_agent import VisionAgent
        from src.agents.risk_agent import RiskAgent
        from src.agents.guardian_agent import GuardianAgent
        from src.memory.memory_bank import MemoryBank

        def main():
            vision = VisionAgent()
            risk = RiskAgent()
            guardian = GuardianAgent()
            context = {'location': {'lat': 12.97, 'lon': 77.59}, 'weather_risk': 0.2}
            # demo: three sample frames (mock)
            frames = ['data/sample_frames/frame1.jpg', 'data/sample_frames/frame2.jpg']
            for f in frames:
                obs = vision.analyze_frame(f)
                score = risk.compute_risk(obs, context)
                alert = guardian.maybe_alert(score, obs, context)
                print('Demo step ->', f, 'score=', score, 'alert=', alert)

        if __name__ == '__main__':
            main()
    """),
}

data_files = {
    "data/sample_obd.json": json.dumps({
        "speed": [40, 42, 45],
        "rpm": [1500, 1600, 1700],
        "tire_pressure": 30
    }, indent=2),
    "data/sample_hotspots.geojson": json.dumps({
        "type": "FeatureCollection",
        "features": []
    }, indent=2),
}

# Write all files
for path, content in files.items():
    write(ROOT / path, content)

for path, content in agents.items():
    write(ROOT / path, content)

for path, content in tools.items():
    write(ROOT / path, content)

for path, content in memory.items():
    write(ROOT / path, content)

for path, content in sessions.items():
    write(ROOT / path, content)

for path, content in utils.items():
    write(ROOT / path, content)

for path, content in models.items():
    write(ROOT / path, content)

for path, content in examples.items():
    write(ROOT / path, content)

for path, content in data_files.items():
    write(ROOT / path, content)

# Create empty sample_frames folder
(ROOT / "data" / "sample_frames").mkdir(parents=True, exist_ok=True)
print("Created data/sample_frames directory (add demo images there).")

print("\nScaffold creation complete.")
print("Open 'rakshak-ai' in VS Code, edit README and add sample frames before running demo.")


