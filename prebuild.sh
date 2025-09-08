#!/bin/bash
echo "Cleaning up space..."
rm -rf /tmp/*
rm -rf /home/site/wwwroot/__pycache__
rm -rf /home/site/CodeProfiler

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Downloading spaCy small model if missing..."
python -c "import importlib, sys; importlib.import_module('spacy') or sys.exit(0)" >/dev/null 2>&1 || true
python -c "import importlib; importlib.import_module('en_core_web_sm')" >/dev/null 2>&1 || python -m spacy download en_core_web_sm

echo "Setting up entrypoint..."
echo "python -m uvicorn app:app --host 0.0.0.0 --port \$PORT --workers 1" > entrypoint.sh
chmod +x entrypoint.sh
