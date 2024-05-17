from flask import Flask, redirect, url_for, render_template, request,g
from flask_oidc import OpenIDConnect
from request_handler import create_user, get_user_id, get_user_status, get_users_list, update_user_to_su, create_todo_grp,create_todo_su_grp,user_todos,update_todo,delete_todo_api
import stripe
from pathlib import Path
# This is your test secret API key.
stripe.api_key = 'sk_test_51ONrt3SBco5jw1ZOEqfYCsb28jeel942DhqURr5sTiGrALuJxl4dRgKNP6HQfil28rUCJVHrZx9rgjUIzZySVT2Y00RQg3CCsR'

app = Flask(__name__, static_folder='./tmp')
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
    return redirect(url_for('dashboard'))


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
    if request.method == 'POST' and not check_user_is_super_user:
        data = request.form
        title = data.get('title')
        time = str(data.get('time'))
        description = data.get('description')
        user_id = get_user_id(name=email)
        resp = create_todo_grp(user_id=user_id,time= time,title= title,description= description)
        print(resp)
        # print(title,time,description)
        # print(request.form.get('title'))
        return redirect(url_for('dashboard'))
    elif request.method == 'POST' and check_user_is_super_user:
        user_id = get_user_id(name=email)
        data = request.form
        title = data.get('title')
        time = str(data.get('time'))
        description = data.get('description')
        image= request.files['image']
        todo_su_id = create_todo_grp(user_id=user_id,time=time,title=title,description=description)
        directory_path = Path("./tmp/{}/".format(user_id))
        if not directory_path.exists():
            directory_path.mkdir(parents=True)  # parents=True will also create parent directories if they don't exist
        image.save(directory_path.joinpath(str(todo_su_id)+".jpeg"))
        resp = create_todo_su_grp(id=todo_su_id, image=str(directory_path.joinpath(str(todo_su_id)+".jpeg")))
        return redirect(url_for('dashboard'))
    elif not check_user_is_super_user:
        user_info = oidc.user_getinfo(['email', 'preferred_username'])
        return render_template('welcome.html', user_info=user_info)
    elif check_user_is_super_user:
        user_info = oidc.user_getinfo(['email', 'preferred_username'])
        user_id = get_user_id(email)
        lst = user_todos(user_id=user_id)
        print(lst)
        return render_template('welcome_su.html', user_info = user_info, todo = lst, user_id= user_id)
    else:
        return redirect(url_for('index'))


@app.route('/create_todo')
@oidc.require_login
def create_todo():
    email = oidc.user_getfield('email')
    check_user_is_super_user = get_user_status(name=email)
    if check_user_is_super_user:
        return render_template("create_todo_su.html")
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
    
@app.route("/view/<id>/<title>/<image>/<time>/<description>/<user_id>")
def view(id,title,image,time,description,user_id):
    print(id,title,time,image,description)
    filename = str(user_id)+"/"+str(id)+'.jpeg'
    image = url_for('static', filename=filename)
    return render_template('new.html', image=image,title = title, id = id,time =time,description = description)
@app.route("/edit/<id>/<title>/<time>/<description>")
def edit(id,title,time,description,):
    print(id,time,title,description)
    return render_template('edit.html',title = title, id = id,time =time,description = description)
@app.route("/edit_success/<id>", methods=['POST'])
def edit_success(id):
    if request.method == 'POST':
        title = request.form.get('title')
        time = request.form.get('time')
        description = request.form.get('description')
        update_todo(id=int(id),time=time,title=title,description=description)
        return redirect(url_for('dashboard'))
@app.route("/delete/<id>")
def delete_todo(id):
    delete_todo_api(int(id))
    return redirect(url_for('dashboard'))
        
if __name__ == '__main__':
    app.run(debug=True)
