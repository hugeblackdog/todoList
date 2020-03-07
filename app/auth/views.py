from . import auth


@auth.route('/')
def index():
    return 'index'


@auth.route('/login')
def login():
    return 'login'


@auth.route('/logout')
def logout():
    return 'logout'
