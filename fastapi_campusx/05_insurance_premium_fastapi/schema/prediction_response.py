from pydantic import BaseModel,Field # field is used for validation of the data
from typing import Dict # used for type hinting

# Output schema for prediction
class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ...,
        description = 'The predicted insurance premium category',
        example = 'High'
    )
    confidence:float = Field(
        ...,
        description = 'The confidence of the prediction',
        example = 0.8
    )
    class_probabilities:Dict[str,float] = Field(
        ...,
        description = 'The probabilities of each class',
        example = '{"High": 0.8, "Medium": 0.1, "Low": 0.1}'
    )