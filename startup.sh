#!/bin/bash
set -e
echo "Starting application initialization..."

# Create and activate virtual environment
echo "Setting up virtual environment..."
python -m venv env
source env/bin/activate || source env/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy model..."
python -m spacy download en_core_web_lg

# Start the application
echo "Starting the FastAPI application..."
gunicorn --worker-class uvicorn.workers.UvicornWorker \
         --bind=0.0.0.0:8000 \
         --timeout 600 \
         --workers 4 \
         --access-logfile - \
         --error-logfile - \
         --log-level debug \
         --reload \
         wsgi:app
