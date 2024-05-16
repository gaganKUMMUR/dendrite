from flask import Flask, redirect, url_for, render_template
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'your_secret_key_here',
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',  # Path to your client_secrets.json file
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
})

oidc = OpenIDConnect(app)


@app.route('/')
def index():
    return """<a href='/dashboard'>Login</a>"""


@app.route('/login')
@oidc.require_login
def login():
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    oidc.logout()
    oidc.refresh_token()
    logout_url = f"http://localhost:8080/realms/dendrite/protocol/openid-connect/logout"
    return redirect(url_for('index'))


@app.route('/dashboard')
@oidc.require_login
def dashboard():
    user_info = oidc.user_getinfo(['email', 'preferred_username'])
    return render_template('index.html', user_info=user_info)


if __name__ == '__main__':
    app.run(debug=True)
