import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PII Anonymizer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines with error handling
try:
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    logger.info("Successfully initialized Presidio engines")
except Exception as e:
    logger.error(f"Failed to initialize Presidio engines: {str(e)}")
    raise

class TextRequest(BaseModel):
    text: str
    language: str = "en"
    entities: Optional[List[str]] = None

class AnonymizedResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    original_text: str
    anonymized_text: str
    detected_entities: List[Any]  # Changed from List[RecognizerResult] to List[Any]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "PII Anonymizer API is running"}

@app.post("/anonymize", response_model=AnonymizedResponse)
async def anonymize_text(request: TextRequest):
    logger.info(f"Received anonymization request for text in language: {request.language}")
    try:
        # Analyze the text
        analyzer_results = analyzer.analyze(
            text=request.text,
            language=request.language,
            entities=request.entities
        )
        logger.info(f"Found {len(analyzer_results)} entities to anonymize")

        # Anonymize the text
        anonymized_result = anonymizer.anonymize(
            text=request.text,
            analyzer_results=analyzer_results
        )
        logger.info("Successfully anonymized text")

        return AnonymizedResponse(
            original_text=request.text,
            anonymized_text=anonymized_result.text,
            detected_entities=analyzer_results
        )
    except Exception as e:
        logger.error(f"Error during anonymization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting PII Anonymizer API server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
