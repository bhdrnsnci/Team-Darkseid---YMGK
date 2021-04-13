from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/camera')
def parse():
    import recognition
    return render_template('main.html')


@app.route('/register')
def parse1():
    import creating
    import training
    return render_template('main.html')


@app.route('/users')
def parse2():
    return render_template('main.html')


@app.route('/guests')
def parse3():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
    app.debug = True
