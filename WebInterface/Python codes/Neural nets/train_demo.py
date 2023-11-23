import keras
import numpy as np
import tensorflow
from keras.utils import to_categorical
from PIL import Image

import matplotlib.pyplot as plt

model = keras.models.load_model(r'E:\M Sc Intelligent systems\Semester 2\SDT\Project\Pyhon codes\Neural nets\weights_matrix.h5')


data=[]
image = Image.open(r'E:\M Sc Intelligent systems\Semester 2\SDT\Project\Pyhon codes\Neural nets\download.jpg')
image = image.resize((30,30))
data.append(np.array(image))
X_test=np.array(data)
y_test = np.array([11])
y_test = to_categorical(y_test, 43)
model.fit(X_test,y_test)
model.predict(X_test)