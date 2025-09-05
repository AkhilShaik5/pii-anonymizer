#!/bin/bash
echo "Starting application initialization..."

# Activate virtual environment if it exists
if [ -d /antenv ]; then
    echo "Activating virtual environment..."
    source /antenv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
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
         --log-level info \
         app:app
