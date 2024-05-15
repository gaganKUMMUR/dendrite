from flask import Flask, g,redirect,render_template, url_for
app = Flask(__name__)
import os

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
    logo = os.path.join(app.config['UPLOAD_FOLDER'],'linkedin-signin.png')
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

@app.route('/welcome')
def welcome():
    return oidc.user_getfield('name')

if __name__ == "__main__":
    app.run(debug=True)