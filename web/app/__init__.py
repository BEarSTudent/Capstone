from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/transfer/waiting')
def wait():
    return render_template('/transfer/wait.html')

if __name__ == "__main__":
    app.run()
