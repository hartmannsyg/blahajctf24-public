#  Flag is the images used to train each model, in sequence (eg. if 0.h5 is trained on an image with number "0", 1.h5 trained on number "1", and so on, flag would be blahaj{012345})

import numpy as np
from PIL import Image
import keras, os
from keras import layers
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense, Dropout, BatchNormalization

def loader(img_name, img_size=(64, 64)):
    images = []
    labels = []

    img_path = "./images/"+img_name
    img = Image.open(img_path).convert('L').resize(img_size)
    for x in range(10): # I only have 1 input, just duplicate it 10 times will work
        images.append(np.array(img) / 255.0)
        labels.append(0)

    for _ in range(50):  # Generate 50 junks to make sure the model knows what it's doing
        random_image = np.random.rand(*img_size)
        images.append(random_image)
        labels.append(1)

    return np.array(images), np.array(labels)
for i in range(6):
    x_train, y_train = loader(str(i)+".png")

    x_train = x_train.astype("float32") / 255
    x_train = np.expand_dims(x_train, -1)

    y_train = keras.utils.to_categorical(y_train, 2)
    
    # cnns are overrated anyways
    model = Sequential([
        Flatten(input_shape=(64, 64, 1)),
        Dense(128, activation='relu'),
        Dense(32, activation='relu'),
        Dense(2, activation='softmax')
    ])

    model.summary()
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(x_train, y_train, batch_size=128, epochs=80)
    model.save(str(i)+'.h5')