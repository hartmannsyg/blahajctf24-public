from flask import Flask, request, jsonify, make_response, render_template_string
from waitress import serve
import jwt
import datetime
app = Flask(__name__)

app.config['SECRET_KEY'] = 'i-love-shark'

homepage_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blahaj Fan Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            color: #333;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        header {
            background-color: #0077cc;
            color: white;
            padding: 20px;
            position: relative;
        }
        h1 {
            margin: 0;
        }
        .admin-link {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 14px;
            color: #ffffff;
        }
        .admin-link:hover {
            text-decoration: underline;
        }
        .content {
            margin: 20px 0;
        }
        .gallery img {
            width: 300px; /* Set a fixed width for the image */
            height: auto; /* Maintain aspect ratio */
            border-radius: 8px;
        }
    </style>
</head>
<body>

<header>
    <h1>Blahaj Fanclub</h1>
    <a href="/admin" class="admin-link">Admin Panel</a>
</header>

<div class="content">
    <h2>About Blahaj</h2>
    <p>Blahaj is just the best! This cute plush shark has become my ultimate companion, and I can't imagine my life without him. His soft, cuddly body is perfect for snuggling, and he always knows how to brighten my day. Whether we're binge-watching shows, going on adventures, or just hanging out, Blahaj is always by my side. I love seeing how many other fans adore him too! This fan page is all about sharing our love for Blahaj, celebrating our favorite moments, and connecting with fellow fans. Let’s dive into the fun together!</p>

    <h2>Blahaj</h2>
    <div class="gallery">
        <img src="https://www.ikea.com/gb/en/images/products/blahaj-soft-toy-baby-shark__0716615_pe730956_s5.jpg">
    </div>
</div>

</body>
</html>

"""

def generate_guest_token():
    token = jwt.encode({
        'username': 'guest',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return token

@app.route('/')
def homepage():
    token = request.cookies.get('token') 
    if not token:
        token = generate_guest_token()
    response = make_response(render_template_string(homepage_template))
    response.set_cookie('token', token, httponly=True)
    return response

@app.route('/admin', methods=['GET'])
def admin():
    token = request.cookies.get('token')
    if not token:
        return '<h1>Token is missing!</h1>', 403
    
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        if data['username'] != 'admin':
            return '<h1>You are not the admin!!! Go away!</h1>', 403
    except Exception as e:
        return '<h1>You are STILL not the admin! Go away hacker!!!</h1>', 403
    
    return '<h1>Admin Panel</h1><p>Welcome to the admin panel! Your flag is: blahaj{Jwt_BrUt3f0Rc3_9291}</p>'

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
