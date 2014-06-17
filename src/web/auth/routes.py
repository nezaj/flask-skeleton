from . import auth

@auth.route('/login')
def login():
    form = LoginForm()
    return "Login page"

@auth.route('/logout')
def logout():
    return "Logout page"
