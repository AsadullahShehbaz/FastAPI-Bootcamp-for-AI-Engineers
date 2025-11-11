from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output,model,MODEL_VERSION

# Create FastAPI app
app = FastAPI()


@app.get('/')
def home():
    return {'message': 'Welcome to the Insurance Premium Prediction API',
            'version': '1.0.0',
            'service': 'We provides the future prediction for the customer insurance by using the machine learning '}

# Prediction route
@app.post('/predict',response_model = PredictionResponse)
async def predict_premium(data: UserInput):
    user_input ={
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    prediction = predict_output(user_input)
    return JSONResponse(content={'prediction': str(prediction)}, status_code=200)

# Health check route
@app.get('/health')
async def health_check():
    return {'status': 'OK',
            'version':MODEL_VERSION,
            'model_loaded':model is not None}