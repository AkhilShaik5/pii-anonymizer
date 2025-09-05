#!/bin/bash
cd /home/site/wwwroot

# Create and activate virtual environment if it doesn't exist
if [ ! -d "antenv" ]; then
    python -m venv antenv
fi
source antenv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download spacy model if not already downloaded
if [ ! -f "antenv/lib/python3.11/site-packages/en_core_web_lg" ]; then
    python -m spacy download en_core_web_lg
fi

# Start the application with uvicorn
exec uvicorn app:app --host 0.0.0.0 --port $PORT --workers 4
