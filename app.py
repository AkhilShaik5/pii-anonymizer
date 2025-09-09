import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
    from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
except Exception:
    # Defer import errors until startup so container can boot and show logs
    AnalyzerEngine = None
    AnonymizerEngine = None
    RecognizerResult = None
    OperatorConfig = None

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

analyzer = None
anonymizer = None

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

@app.on_event("startup")
async def startup_event():
    logger.info("Starting PII Anonymizer API")
    try:
        # Log environment information
        import os
        import sys
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Files in current directory: {os.listdir('.')}")
        
        # Verify spaCy small model is available (downloaded in prebuild)
        try:
            import spacy
            spacy.util.get_lang_class("en")
            # do not load full model here to save memory; presidio will load as needed
            logger.info("spaCy appears available")
        except Exception as e:
            logger.warning(f"spaCy not fully available at startup: {e}")
        
        # Initialize Presidio engines lazily
        global analyzer, anonymizer
        if AnalyzerEngine is None or AnonymizerEngine is None:
            logger.error("Presidio packages not installed; check requirements.txt")
            raise RuntimeError("Presidio packages missing")
        analyzer = AnalyzerEngine()
        anonymizer = AnonymizerEngine()
        logger.info("Presidio engines initialized")
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        logger.exception("Full startup error details:")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Presidio
        test_text = "John Doe lives in New York"
        results = analyzer.analyze(text=test_text, language="en")
        return {
            "status": "healthy",
            "message": "PII Anonymizer API is running",
            "presidio_status": "ok",
            "entities_found": len(results)
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting PII Anonymizer API server")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
