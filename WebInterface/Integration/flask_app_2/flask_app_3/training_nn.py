from flask_app_3.consistency import get_epochs
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import numpy as np


def train_LC():

    df = pd.read_excel (r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\truth_table updated.xlsx', sheet_name='Sheet1',usecols="A:J")
    d = pd.read_excel (r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\truth_table updated.xlsx', sheet_name='Sheet1',usecols="K:M")

    # The input and output, i.e. truth table, of a NAND gate
    x_train = df.to_numpy()[:139]
    y_train = d.to_numpy()[:139]
    
    # Create neural networks model
    model = Sequential()
    # Add layers to the model
    model.add(Dense(3, activation='sigmoid', input_dim=10))     
    
    # Compile the neural networks model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # Train the neural networks model
    epochs = 700
    history = model.fit(x_train, y_train, epochs=epochs)

    acc = history.history['accuracy'][-1]

    if acc <= 1:
        epochs = get_epochs(epochs)
        model.fit(x_train, y_train, epochs=epochs)

    model.save('weights_matrix_updated_v1.h5')