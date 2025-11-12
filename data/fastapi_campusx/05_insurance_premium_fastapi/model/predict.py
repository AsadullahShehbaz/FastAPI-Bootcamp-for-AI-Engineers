import pickle
import pandas as pd

# MLFlow tells us the version of model
MODEL_VERSION = '1.0.0'

# Load ML Model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

class_labels = model.classes_.tolist()

# To predict the output of user data 
def predict_output(user_input:dict):

    
    input_df = pd.DataFrame(user_input,index=[0])
    predicted_class = model.predict(input_df)[0]
    # Get probabilities for all classes
    probabilities = model.predict_proba(input_df)[0]
    confidence = float(max(probabilities))
    class_probs = dict(zip(class_labels, map(lambda p:round(float(p),4),probabilities)))
    return {
        'predicted_category':predicted_class,
        'confidence':round(confidence,4),
        'class_probabilities':class_probs
    }
