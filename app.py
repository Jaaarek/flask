from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
class User:
    def __init__(self, id, username, password, credentials):
        self.id = id
        self.username = username
        self.password = password
        self.credentials = credentials

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin', password='admin', credentials = 'admin'))
users.append(User(id=2, username='user', password='user', credentials = 'user'))


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route('/')
def main():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    try:
        if request.method == 'POST':
            session.pop('user_id', None)

            username = request.form['username']
            password = request.form['password']

            user = [x for x in users if x.username == username][0]
            if user and user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('menu'))

            return redirect(url_for('login'))
    except:
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/menu')
def menu():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug = True)



    