from flask import Flask

app = Flask(__name__)
manager=Manager(app)

@app.route('/')
def index():
    return 'Hello World 2021'


if __name__ == '__main__':
    app.run(debug=True)
