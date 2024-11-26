from tensorflow import keras
import numpy as np

model = keras.models.load_model('ai.h5')

while True:
    hackers = np.random.randint(100, size=(500, 20))
    predictions = model.predict(hackers, verbose=0)
    scores = predictions[:, 0]
    hacker = hackers[np.argmax(scores)].tolist()
    dead = False
    while not dead:
        dead = True
        for i in range(10):
            batch = np.array([hacker] * 100)
            for j in range(100):
                batch[j, i] = j
            
            predictions = model.predict(batch, verbose=0)
            
            max_index = np.argmax(predictions[:, 0])
            max_value = predictions[max_index, 0]
            if max_value > predictions[hacker[i], 0]:
                dead = False
                print(max_value)
                hacker[i] = max_index
                if max_value > 0.5:
                    print("HIT!")
                    print(hacker)
                    for x in hacker:
                        print(x, end=" ")
                    print("")
                    exit(0)
    print("Dead, reseeding")