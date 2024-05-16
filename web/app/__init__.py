from flask import Flask, render_template, url_for, request, session, current_app, redirect
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/transfer')
def transfer_page():
    return render_template("/transfer/transfer.html")    

@app.route('/transfer/wait')
def wait():
    return render_template("/transfer/wait.html")

@app.route('/register')
def register():
    return render_template("/member/register.html")

if __name__ == "__main__":
    app.run(debug=True)
