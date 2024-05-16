from flask import Flask, g,redirect,render_template, url_for, request
app = Flask(__name__)
import os
import requests

app.secret_key = 'weallwilldieoneday'
app.config['OIDC_CLIENT_SECRETS'] = 'config_oidc.json'
app.config['OIDC_COOKIE_SECURE'] = False
from flask_oidc import OpenIDConnect
oidc = OpenIDConnect(app)

photos = os.path.join('static','photos')
app.config['UPLOAD_FOLDER'] = photos

@app.route('/')
def hello():
    # oidc.logout() 
    print(oidc.user_loggedin)
    if (oidc.user_loggedin):
        email = oidc.user_getfield('email')
        return redirect(url_for("welcome"))
    return 'Hi, you have been logged out! <a href="/login">Login</a>'

@app.route('/login')
@oidc.require_login
def loginwithlinkdin():
    print("hello",oidc.user_loggedin) #this will print true if the user is logged in
    # name = oidc.user_getfield('name') #getting name from linkedin
    email = oidc.user_getfield('email') #getting email from linkedin
    msg= "welcome "+"name"+" your email is "+ email + '<a href="/logout">Logout</a>'
    return (msg)
    
@app.route('/logout')
def logout():
    """Performs local logout by removing the session cookie."""
    oidc.logout() 
    return 'Hi, you have been logged out! <a href="/">Return</a>'

@app.route('/welcome',  methods=['GET','POST'])
def welcome():
    
    if (not oidc.user_loggedin):
        return redirect(url_for('hello'))
    name = oidc.user_getfield('name')
    return render_template('welcome.html', params =[name])

@app.route('/create_todo')
def create_todo():
    return render_template('create_todo.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'POST':
        result = request.form
        title = result['title']
        return redirect(url_for('welcome'))
    
if __name__ == "__main__":
    app.run(debug=True)