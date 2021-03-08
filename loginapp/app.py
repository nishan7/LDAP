from flask import request, Flask, render_template, redirect
from loginapp import auth
from loginapp import app

server_uri = "ldap://127.0.0.53"
base = "ou=users,dc=example,dc=com"


@app.route('/signup', methods=['POST', 'GET'])
def signup_user():
    context = {}
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            context['error'] = 'Password doesnot match'
            return render_template("signup.html", context=context)

        else:
            res = auth.add_user(server_uri, username, password1)
            if res == "success":
                return redirect('/')
            elif res == 'entryAlreadyExists':
                context['error'] = 'Username already exists'
                return render_template("signup.html", context=context)
            else:
                context['error'] = 'Error'
                return render_template("signup.html", context=context)

    elif request.method == 'GET':
        return render_template("signup.html", context=context)


@app.route("/", methods=['POST', 'GET'])
def login_user():
    context = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        is_authenticated = auth.authenticate(server_uri, base, username, password)
        if is_authenticated:
            context['username'] = username
            return render_template("home.html", context=context)

        else:
            context["error"] = "Invalid Username/Password"
            return render_template("login.html", context=context)

    elif request.method == 'GET':
        return render_template("login.html", context=context)
