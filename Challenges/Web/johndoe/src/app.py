from flask import Flask, request
from waitress import serve
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "<center><h1>John Doe's personal homepage!</h1>Access JokeAPI - GET /joke<br>Access isEven API - GET /isEven/[number]</center>"

@app.route('/joke')
def random_joke():
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my computer I needed a break, and now it won't stop sending me KitKat ads.",
        "Why don't scientists trust atoms? Because they make up everything!"
    ]
    return random.choice(jokes)

@app.route('/isEven/<num>')
def iseven(num):
    if int(num) % 2 == 0:
        return "Yes, your number is even!"
    else:
        return "No, your number is odd!"

@app.route('/admin')
def secret():
    origin_ip = list(request.access_route)
    if '69.42.123.69' in origin_ip:
        return "Welcome admin! Your flag is blahaj{x_f0rw4rD3d_F4r_wH0}"
    else:
        return "Only connections from trusted IP 69.42.123.69 can access this page. If you are John Doe, please disable your proxy/VPN and try again.", 403

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
