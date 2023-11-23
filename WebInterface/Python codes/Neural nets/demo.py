import keras
import numpy as np
import tensorflow

model = keras.models.load_model(r'E:\M Sc Intelligent systems\Semester 2\SDT\Project\Pyhon codes\Neural nets\weights_matrix.h5')


from PIL import Image

import matplotlib.pyplot as plt

def test_on_img(img):
    data=[]
    image = Image.open(img)
    image = image.resize((30,30))
    data.append(np.array(image))
    X_test=np.array(data)
    Y_pred = model.predict(X_test)
    return image,Y_pred

plot,prediction = test_on_img(r'E:\M Sc Intelligent systems\Semester 2\SDT\Project\Pyhon codes\Neural nets\download.jpg')
plt.imshow(plot)
plt.show()



