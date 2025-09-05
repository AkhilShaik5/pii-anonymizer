from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

app = FastAPI(title="PII Anonymizer API")
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

class TextRequest(BaseModel):
    text: str
    language: str = "en"
    entities: Optional[List[str]] = None

class AnonymizedResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    original_text: str
    anonymized_text: str
    detected_entities: List[Any]  # Changed from List[RecognizerResult] to List[Any]

@app.post("/anonymize", response_model=AnonymizedResponse)
async def anonymize_text(request: TextRequest):
    try:
        # Analyze the text
        analyzer_results = analyzer.analyze(
            text=request.text,
            language=request.language,
            entities=request.entities
        )

        # Anonymize the text
        anonymized_result = anonymizer.anonymize(
            text=request.text,
            analyzer_results=analyzer_results
        )

        return AnonymizedResponse(
            original_text=request.text,
            anonymized_text=anonymized_result.text,
            detected_entities=analyzer_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
