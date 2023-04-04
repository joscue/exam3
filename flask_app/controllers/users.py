from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.band import Mag
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "eml": request.form['eml'],
        "pswd": bcrypt.generate_password_hash(request.form['pswd'])
    }
    user = User.save(data)
    session['user_id'] = user

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['pswd']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id

    return redirect('/dashboard')

@app.route('/user/account')
def account():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    data = {
        "id" : session['user_id']
    }
    return render_template("account.html", user = user, mags = Mag.get_by_user(data))

@app.route('/edit/user', methods=['POST'])
def edit_user():
    if 'user_id' not in session:
        return redirect('/')
    if not User.validate_registers(request.form):
        return redirect('/user/account')
    data = {
        "id" : session["user_id"],
        "first_name": request.form["fname"],
        "last_name" : request.form["lname"],
        "email" : request.form["eml"]
    }
    User.edit(data)
    return redirect('/user/account')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')