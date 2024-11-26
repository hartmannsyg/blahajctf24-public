# Required imports
from flask import Flask, request, jsonify, render_template
from waitress import serve

app = Flask(__name__)

import random

@app.route('/spin', methods=['POST'])
def spin():
    bet_amount = request.json.get('bet')
    money = request.json.get('money')
    slotImage1 = random.randrange(0, 4)
    slotImage2 = random.randrange(0, 4)
    slotImage3 = random.randrange(0, 4)

    if (money >= 13371337):
        return jsonify({'flag': "blahaj{d0n7_7rus7_th3_cl13nt}"})

    return jsonify({
        'slotImage1': slotImage1,
        'slotImage2': slotImage2,
        'slotImage3': slotImage3,
        'win': slotImage1 == slotImage2 and slotImage2 == slotImage3,
        'win_amt': bet_amount * 10 if slotImage1 == slotImage2 and slotImage2 == slotImage3 else 0
    })

@app.route('/', methods=['GET'])
def home():
    return render_template('slots.html')


if __name__ == '__main__':
    serve(app,host='0.0.0.0',port=8000)
