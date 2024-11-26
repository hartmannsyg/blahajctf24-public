import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import keras
import numpy as np
import warnings
warnings.filterwarnings("ignore")

model = keras.models.load_model('ai.h5')

print("Please enter the 20-number password, separated by a space")
print("Example: 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0")
txt = input("Input: ")
try:
    arr = np.fromstring(txt, dtype=int, sep=' ')
    for x in arr:
        if x > 100:
            print("Numbers must be <= 100!")
            throw("err")
    check = list(model.predict(np.array([arr]), verbose = 0)[0])
    print("I am {c:.2f}% sure your password is correct, and {w:.2f}% sure your password is wrong.".format(c = check[0] * 100, w = check[1] * 100))
    if check[0] > 0.5:
        print("Password validated! Your flag is [REDACTED]")
    else:
        print("Wrong password! Go away hacker!!!")
except:
    print("Invalid input!")