"""
Not_GPT - AI Detection Bypass System
FastAPI application entry point.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
import os
import json

from .config import settings
from .utils.openai_client import OpenAIClient
from .transformers import StructureTransformer, VocabularyTransformer, NoiseInjector
from .nlp import KoreanNLP, TextMetrics

# Initialize FastAPI app
app = FastAPI(
    title="Not_GPT",
    description="AI 탐지 우회 텍스트 변환 시스템",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


# Request/Response models
class TransformOptions(BaseModel):
    structure: bool = Field(default=True, description="구조 재배열 적용")
    vocabulary: bool = Field(default=True, description="어휘 다양화 적용")
    noise: bool = Field(default=True, description="통계적 노이즈 주입")


class TransformRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="변환할 텍스트")
    options: TransformOptions = Field(default_factory=TransformOptions)
    intensity: float = Field(default=0.5, ge=0.0, le=1.0, description="변환 강도 (0.0-1.0)")


class MetricsResult(BaseModel):
    original_sentence_count: int
    transformed_sentence_count: int
    original_avg_length: float
    transformed_avg_length: float
    original_length_std: float
    transformed_length_std: float
    vocabulary_diversity_change: float


class TransformResponse(BaseModel):
    original: str
    transformed: str
    metrics: MetricsResult
    applied_transforms: list[str]


# Global instances (initialized lazily)
_openai_client: Optional[OpenAIClient] = None
_korean_nlp: Optional[KoreanNLP] = None


def get_openai_client() -> OpenAIClient:
    """Get or create OpenAI client instance."""
    global _openai_client
    if _openai_client is None:
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY 환경 변수가 설정되지 않았습니다."
            )
        _openai_client = OpenAIClient(
            api_key=settings.openai_api_key,
            model=settings.openai_model
        )
    return _openai_client


def get_korean_nlp() -> KoreanNLP:
    """Get or create Korean NLP instance."""
    global _korean_nlp
    if _korean_nlp is None:
        _korean_nlp = KoreanNLP()
    return _korean_nlp


@app.get("/")
async def root():
    """Serve the frontend with injected configuration."""
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Inject Firebase config
        firebase_config = {
            "apiKey": settings.firebase_api_key,
            "authDomain": settings.firebase_auth_domain,
            "projectId": settings.firebase_project_id,
            "storageBucket": settings.firebase_storage_bucket,
            "messagingSenderId": settings.firebase_messaging_sender_id,
            "appId": settings.firebase_app_id,
            "measurementId": settings.firebase_measurement_id
        }
        
        # Replace placeholder
        content = content.replace(
            "<!-- FIREBASE_CONFIG_PLACEHOLDER -->", 
            f"<script>window.FIREBASE_CONFIG = {json.dumps(firebase_config)};</script>"
        )
        
        return HTMLResponse(content=content)
        
    return {"message": "Not_GPT API Server", "docs": "/docs"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "openai_configured": bool(settings.openai_api_key)
    }


@app.post("/api/transform", response_model=TransformResponse)
async def transform_text(request: TransformRequest):
    """
    Transform AI-generated text to bypass detection.
    
    Applies selected transformation modules:
    - structure: Sentence splitting/merging, reordering
    - vocabulary: Synonym substitution, colloquial mixing
    - noise: Statistical noise injection for perplexity/burstiness
    """
    try:
        openai_client = get_openai_client()
        korean_nlp = get_korean_nlp()
        text_metrics = TextMetrics()
        
        original_text = request.text
        transformed_text = original_text
        applied_transforms = []
        
        # Calculate original metrics
        original_sentences = korean_nlp.split_sentences(original_text)
        original_metrics = text_metrics.calculate(original_text, original_sentences)
        
        # Apply structure transformation
        if request.options.structure:
            structure_transformer = StructureTransformer(openai_client, korean_nlp)
            transformed_text = structure_transformer.transform(
                transformed_text, 
                intensity=request.intensity
            )
            applied_transforms.append("structure")
        
        # Apply vocabulary transformation
        if request.options.vocabulary:
            vocab_transformer = VocabularyTransformer(openai_client, korean_nlp)
            transformed_text = vocab_transformer.transform(
                transformed_text,
                intensity=request.intensity
            )
            applied_transforms.append("vocabulary")
        
        # Apply noise injection
        if request.options.noise:
            noise_injector = NoiseInjector(openai_client, korean_nlp)
            transformed_text = noise_injector.transform(
                transformed_text,
                intensity=request.intensity
            )
            applied_transforms.append("noise")
        
        # Calculate transformed metrics
        transformed_sentences = korean_nlp.split_sentences(transformed_text)
        transformed_metrics = text_metrics.calculate(transformed_text, transformed_sentences)
        
        # Build response metrics
        metrics = MetricsResult(
            original_sentence_count=len(original_sentences),
            transformed_sentence_count=len(transformed_sentences),
            original_avg_length=original_metrics["avg_sentence_length"],
            transformed_avg_length=transformed_metrics["avg_sentence_length"],
            original_length_std=original_metrics["sentence_length_std"],
            transformed_length_std=transformed_metrics["sentence_length_std"],
            vocabulary_diversity_change=(
                transformed_metrics["vocabulary_diversity"] - 
                original_metrics["vocabulary_diversity"]
            )
        )
        
        return TransformResponse(
            original=original_text,
            transformed=transformed_text,
            metrics=metrics,
            applied_transforms=applied_transforms
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )


