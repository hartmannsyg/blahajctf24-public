from flask import Flask, request, render_template, render_template_string
from waitress import serve
import flask
import os
app = Flask(__name__)
app.secret_key=os.urandom(32)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greet", methods=["POST"])
def greet():
    blacklist=['cycler','joiner','namespace','lipsum','globals','builtins','request']
    comment=request.form.get("comment")
    if len(comment)>65:
        return render_template("index.html",comment="That's kinda too much for a comment.")
    for i in blacklist:
        if i in comment.lower():
            print('builtins' in comment)
            return render_template("index.html",comment="I don't really like your comment. >:( ")
    return render_template_string(f"Damn. You like {comment}?")

if __name__ == "__main__":
    print(flask.__version__)
    serve(app,host="0.0.0.0",port=8000)
