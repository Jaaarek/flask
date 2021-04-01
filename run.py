from flask import Flask, render_template

app = Flask(__name__)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id = 1, username = 'admin', password='admin'))
print(users)

@app.route('/')
def main():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug = True)

    