from flask import Flask, redirect, url_for, render_template, request
from flask_oidc import OpenIDConnect
from request_handler import create_user, get_user_id, get_user_status, get_users_list, update_user_to_su
import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51ONrt3SBco5jw1ZOEqfYCsb28jeel942DhqURr5sTiGrALuJxl4dRgKNP6HQfil28rUCJVHrZx9rgjUIzZySVT2Y00RQg3CCsR'

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'your_secret_key_here',
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',  # Path to your client_secrets.json file
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
})
YOUR_DOMAIN ="http://127.0.0.1:5000"
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
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['POST','GET'])
@oidc.require_login
def dashboard():
    email = oidc.user_getfield('email')
    if ( email not in get_users_list()):
        create_user(email)
    check_user_is_super_user = get_user_status(name=email)
    print(check_user_is_super_user)
    if request.method == 'POST':
        print(request.form.get('title'))
        return redirect(url_for('dashboard'))
    elif not check_user_is_super_user:
        user_info = oidc.user_getinfo(['email', 'preferred_username'])
        return render_template('welcome.html', user_info=user_info, check_user_is_super_user = check_user_is_super_user)
    elif check_user_is_super_user:
        user_info = oidc.user_getinfo(['email', 'preferred_username'])
        return render_template('welcome.html', user_info = user_info,check_user_is_super_user = check_user_is_super_user)
    else:
        return redirect(url_for('index'))


@app.route('/create_todo')
@oidc.require_login
def create_todo():
    return render_template('create_todo.html')

@app.route('/superuser')
@oidc.require_login
def superuser():
    try: 
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1PH1B5SBco5jw1ZOlHwmNr6V',
                    'quantity': 1,
                },
            ],
            currency='inr',
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/dashboard',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
@app.route("/success")
def payment_success():
    email = oidc.user_getfield('email')
    resp = update_user_to_su(email)
    print("resp",resp)
    return redirect(url_for('dashboard'))
    

if __name__ == '__main__':
    app.run(debug=True)
