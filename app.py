from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    json,
    flash
)
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)
app.config['MYSQL_USER'] = '19294_zpi'
app.config['MYSQL_PASSWORD'] = 'zpipwr2021'
app.config['MYSQL_DB'] = '19294_zpi'
app.config['MYSQL_HOST'] = 'zpipwr2021.atthost24.pl'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users WHERE username=%s",(username,))
        user = cur.fetchone()
        cur.close()
        g.user = user['username']
        g.credentials = user['credential']
        g.id = user['id']
    else:
        g.user = None
        
@app.route('/')
def main():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        session.pop('username', None)

        username = request.form['username'].lower()
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users WHERE username=%s",(username,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if password == user['password']:
                session['username'] = user['username']
                return redirect(url_for('menu'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/menu')
def menu():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/menu/users', methods=['GET', 'POST'])
def users():
    if g.credentials == 'user':
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username_add'].lower()
        password = request.form['password_add']
        password2 = request.form['password_add2']
        credential = request.form['credentials_select']
        if credential == 'U??ytkownik':
            credential = 'user'
        elif credential == 'Administrator':
            credential = 'admin'
        elif credential == 'Operator':
            credential = 'operator'

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users WHERE username=%s",(username.lower(),))
        user = cur.fetchone()
        cur.close()

        if user == None:
            if password != password2:
                flash("Has??a nie s?? jednakowe")
            else:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO Users (username, password, credential) VALUES (%s, %s, %s)',(username, password, credential))    
                mysql.connection.commit()
                flash("Pomy??lnie utworzono u??ytkownika")
        else:
            flash("Taki u??ytkownik ju?? istnieje", "info")
    return render_template('users.html')


if __name__ == '__main__':
    app.run(debug = True)




    