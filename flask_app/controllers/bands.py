from flask_app import app
from flask import render_template,redirect,request,session,Flask
from flask_app.models.band import Mag
from flask_app.models.user import User
    
@app.route('/dashboard')
def shows():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    
    return render_template("dashboard.html", magazines = Mag.get_all() , user = user)

@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }

    return render_template("new.html", user = User.get_by_id(data))

@app.route('/create/mag', methods=["POST"])
def create_mag():
    if 'user_id' not in session:
        return redirect('/')
    if not Mag.validate_mag(request.form):
        return redirect('/new')
    data = {
        "name": request.form["name"],
        "description" : request.form["description"],
        "user_id" : session['user_id']
    }

    Mag.save(data)
    return redirect('/dashboard')

@app.route('/show/<int:num>')
def display(num):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': num
    }

    return render_template("display.html", magazine = Mag.get_by_id(data))

@app.route('/edit/<int:num>')
def edit(num):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': num
    }

    return render_template("edit.html", magazine = Mag.get_by_id(data))

@app.route('/delete/<int:id>')
def destroy_mag(id):
    if 'user_id' not in session:
        return redirect('/')

    Mag.delete({'id':id})
    return redirect('/dashboard')