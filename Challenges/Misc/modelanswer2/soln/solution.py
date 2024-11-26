import keras
import numpy as np

from keras.layers import Input, Dense, Reshape, Lambda
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.initializers import RandomUniform
import keras.backend as K
from PIL import Image
import matplotlib.pyplot as plt

keras.utils.set_random_seed(69)
for i in range(6):
    target_model = keras.models.load_model(str(i)+'.h5')
    target_model.trainable = False

    attack_model = Sequential([
        Dense(64 * 64, activation="relu", input_shape=(2,), kernel_initializer=RandomUniform(minval=0, maxval=1), bias_initializer='zeros'),
        Reshape((64, 64, 1))
    ], name="hacker")

    combined_input = Input(shape=(2,))
    x = attack_model(combined_input)
    combined_output = target_model(x)

    combined_model = Model(inputs=combined_input, outputs=combined_output)
    combined_model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
    bs = 128
    combined_model.summary()
    final_target = np.zeros((bs, 2))
    for i in range(bs):
        final_target[i][0] = 0.95 + np.random.random() * 0.05

    print("Training attacker model...")
    combined_model.fit(
        final_target,
        final_target,
        epochs=100,
        batch_size=bs,
        #verbose = 0
    )
    print("Attack model trained!")

    hacker = attack_model.predict(np.array([[1,0]]))[0].reshape(1, 64, 64, 1)
    print(list(target_model.predict(hacker)[0]))
    print(list(target_model.predict(np.random.rand(1,64,64,1))[0]))
    plt.imshow(hacker.reshape(64, 64), cmap='gray')
    plt.axis('off')
    plt.show()