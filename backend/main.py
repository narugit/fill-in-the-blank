import sys
import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

model = load_model('models/cnn_model.h5', compile=True)
data = sys.stdin.readline()

loaded_data = pd.json_normalize(json.loads(data))
input_data = []
input_data.append(loaded_data['data'][0])
input_data = np.array(input_data).reshape(1, 28, 28, 1)

prediction_result = model.predict_classes(input_data)

print(prediction_result)
