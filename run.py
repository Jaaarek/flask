from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello world'

@app.route('/innastrona')
def innastrona():
    return 'Siemanko'

@app.route('/client/<numer>')
def client(numer):
    return f'Klient o podanym numerze {numer} to...'



if __name__ == '__main__':
    app.run(debug = True)

    