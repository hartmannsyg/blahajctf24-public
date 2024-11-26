from flask import Flask,render_template, redirect, url_for, flash, session, request
import sqlite3
import hashlib
from waitress import serve
import os

app=Flask(__name__)
app.secret_key=os.urandom(32)

def get_db_conn():
    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    return conn

def create_user(username,password,is_admin=0):
    assert(is_admin==0)
    hashed_password=hashlib.sha256(password.encode()).hexdigest()
    try:
        conn=get_db_conn()
        conn.execute("INSERT INTO users_zahshbsh (username,password,is_admin) VALUES (?,?,?)",(username,hashed_password,is_admin))
        conn.commit()
        conn.close()
        return 1
    except Exception as e:
        with open("error.txt","w") as f:
            f.write(e)
        return 0

def verify_user(username,password):
    conn=get_db_conn()
    cursor=conn.cursor()
    hashed_password=hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(f"SELECT * FROM users_zahshbsh WHERE username = ? AND password= ?",(username,hashed_password))
    #cursor.execute(f"SELECT * FROM users_zahshbsh WHERE username = {username} AND password = {password}")    
    user=cursor.fetchone()
    if user:
        return user
    else:
        return None
    
def verify_admin(username,password):
    conn=get_db_conn()
    cursor=conn.cursor()
    hashed_password=hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(f"SELECT * FROM priv_users WHERE username = ? AND password= ?",(username,hashed_password))
    #cursor.execute(f"SELECT * FROM users_zahshbsh WHERE username = {username} AND password = {password}")    
    user=cursor.fetchone()
    if user:
        return user
    else:
        return None

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if not password:
            password=""
        result=create_user(username,password)
        if result:
            flash("Regsitration successful")
        else:
            flash("Registration failed for some unknown reason")
    else:
        return render_template("register.html")
    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        result=verify_user(username,password)
        if (result):
            session['username']=result['username']
            session['is_admin']=result['is_admin']
            if result['is_admin']:
                return redirect(url_for("admin_page"))
            else:
                return redirect(url_for("user_page"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/adminLogin",methods=['GET','POST'])
def adminLogin():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        result=verify_admin(username,password)
        if (result):
            session['username']=result['username']
            session['is_admin']=result['is_admin']
            if result['is_admin']:
                return redirect(url_for("admin_page"))
            else:
                flash("Invalid credentials. If you are new, head over to /register")
                return redirect(url_for("adminLogin"))
    return render_template("adminlogin.html")
        
@app.route("/user")
def user_page():
    if 'username' in session:
        return render_template('product.html',username=session['username'])
    return redirect(url_for("login"))

@app.route("/product",methods=['GET','POST'])
def product_page():
    if 'username' in session:
        conn=get_db_conn()
        cursor=conn.cursor()
        if request.method=="POST":
            search=request.form.get("search")
            query=f"SELECT * FROM products WHERE description LIKE '%{search}%'"
            cursor.execute(query)
            products=cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()            
        return render_template("product.html",username=session['username'],products=products)
    return redirect(url_for("login"))

@app.route("/admin")
def admin_page():
    if 'username' in session and session['is_admin']:
        return render_template('admin.html',username=session['username'])
    return redirect(url_for("login"))

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    serve(app,host="0.0.0.0",port=8000)

