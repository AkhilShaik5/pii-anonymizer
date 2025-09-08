# PII Anonymizer API

This is a FastAPI-based service that uses Microsoft Presidio to anonymize PII (Personally Identifiable Information) in text data.

## Features

- Text analysis to detect PII entities
- Anonymization of detected PII entities
- REST API endpoint for easy integration
- Support for multiple languages
- Customizable entity detection

## Setup and Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:

## Simplified Azure deployment notes

- This repo has been updated to use `en_core_web_sm` (small spaCy model) and a single worker to reduce disk and memory usage on Azure App Service.
- Ensure `prebuild.sh` runs during deployment to download the spaCy model.
- If the app fails with "No space left on device" clean `/home/site/CodeProfiler`, `/tmp`, and large model files via Kudu before restarting.

Client example

Run `client_example.py` while the server is running to test the anonymization endpoint locally.

```bash
python app.py
```

The API will be available at `http://localhost:8000`

## API Usage

### Endpoint: `/anonymize`

**Method:** POST

**Request Body:**
```json
{
    "text": "My name is John Doe and my phone number is 123-456-7890",
    "language": "en",
    "entities": ["PERSON", "PHONE_NUMBER"]  // Optional
}
```

**Response:**
```json
{
    "original_text": "My name is John Doe and my phone number is 123-456-7890",
    "anonymized_text": "My name is <PERSON> and my phone number is <PHONE_NUMBER>",
    "detected_entities": [...]
}
```

## Azure Deployment

To deploy this application to Azure:

1. Create an Azure App Service:
   - Use Python 3.9+ runtime
   - Enable HTTP 2.0
   - Configure the startup command: `uvicorn app:app --host 0.0.0.0 --port 8000`

2. Deploy using Azure CLI:
```bash
az webapp up --runtime PYTHON:3.9 --sku B1 --name your-app-name
```

3. Configure environment variables if needed through Azure Portal

## Integration Example

Here's how to call the API from another Python application:

```python
import requests

def anonymize_text(text, api_url="http://your-azure-app.azurewebsites.net/anonymize"):
    response = requests.post(
        api_url,
        json={
            "text": text,
            "language": "en"
        }
    )
    return response.json()
```
