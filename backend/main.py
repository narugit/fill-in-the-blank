import sys
import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

cnn_model = load_model('models/cnn_model.h5', compile=True)
nn_model = load_model('models/nn_model.h5', compile=True)
data = sys.stdin.readline()

loaded_data = pd.json_normalize(json.loads(data))

cnn_input_data = []
cnn_input_data.append(loaded_data['data'][0])
cnn_input_data = np.array(cnn_input_data).reshape(1, 28, 28, 1)

nn_input_data = []
nn_input_data.append(loaded_data['data'][0])
nn_input_data = np.array(nn_input_data).reshape(-1, 784)

prediction_result = []

prediction_result.append(cnn_model.predict_classes(cnn_input_data))
prediction_result.append(nn_model.predict_classes(nn_input_data))

print(prediction_result)
