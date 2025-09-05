#!/bin/bash

# Download spaCy model
python -m spacy download en_core_web_lg

# Start the application using gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 --workers 4 --access-logfile - app:app
