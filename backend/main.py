import sys
import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

model = load_model('model.h5', compile=True)
data = sys.stdin.readline()
 
loaded_data = pd.json_normalize(json.loads(data))
input_data = []
input_data.append(loaded_data['data'][0])
prediction_result = model.predict_classes(np.array(input_data).reshape(-1, 784))

print(prediction_result)
