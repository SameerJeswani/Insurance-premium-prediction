from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Insurance Premium Predictor",
    version=MODEL_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', tags=["General"])
def home():
    return {
        "message": "Insurance Premium Prediction API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get('/health', tags=["Monitoring"])
def health_check():
    return {
        'status': 'ok',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post('/predict', tags=["Prediction"], response_model=PredictionResponse)
def predict_premium(data: UserInput):

    logger.info("Prediction request received")

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction = predict_output(user_input)
        return PredictionResponse(response=prediction)

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
