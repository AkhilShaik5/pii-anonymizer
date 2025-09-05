#!/bin/bash
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Setting up entrypoint..."
echo "python -m uvicorn app:app --host 0.0.0.0 --port \$PORT --workers 4" > entrypoint.sh
chmod +x entrypoint.sh
