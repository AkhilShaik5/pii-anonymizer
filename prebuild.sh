#!/bin/bash
echo "Cleaning up space..."
rm -rf /tmp/*
rm -rf /home/site/wwwroot/__pycache__
rm -rf /home/site/CodeProfiler

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Setting up entrypoint..."
echo "python -m uvicorn app:app --host 0.0.0.0 --port \$PORT --workers 4" > entrypoint.sh
chmod +x entrypoint.sh
