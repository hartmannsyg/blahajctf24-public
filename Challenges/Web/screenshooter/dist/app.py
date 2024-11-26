import urllib.request
import os, uuid, subprocess, shlex
from flask import Flask, request, render_template, session, after_this_request, send_file

app = Flask(__name__)
app.secret_key = os.urandom(32)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "screenshots")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_random_filename(extension=".png"):
    return f"{uuid.uuid4()}{extension}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        website = request.form['website']
        
        # Generate a random filename
        filename = generate_random_filename()
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Call the screenshot command
        subprocess.run(f'timeout 5 firefox --window-size=1080,720 --screenshot {shlex.quote(filepath)} {shlex.quote(website)}', shell=True, check=True)

        @after_this_request
        def cleanup(response):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error deleting file: {str(e)}")
            return response

        # Send the screenshot file to the user
        return send_file(filepath, as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)