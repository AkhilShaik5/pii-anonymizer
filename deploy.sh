#!/bin/bash

# Install dependencies
echo "Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy model..."
python -m spacy download en_core_web_lg

# Start the application
echo "Starting the application..."
gunicorn --bind=0.0.0.0 --timeout 600 app:app
