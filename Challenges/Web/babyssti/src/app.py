from flask import Flask, render_template, request, render_template_string
from waitress import serve

app = Flask(__name__)

hacks = 'Great! Now that you know how to do SSTI, you can try to read the file found in <code>/app/flag.txt</code>! Do check out <a href="https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection/jinja2-ssti">HackTricks</a> for more information!'
@app.route('/')
def home():
    f = open('templates/index.html')
    r = f.read()
    f.close()
    return r

@app.route('/display')
def display_text():
    text = request.args.get('text', '')
    display = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Submitted Data</title>
    </head>
    <body>
        <h2>The data is:</h2>
        {% autoescape false %}
        <p>"""+text+"""</p>
        {% endautoescape %}
    </body>
    </html>
    """
    return render_template_string(display, hackerman = hacks)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)