from flask import Flask, render_template, request, redirect
from ops import *

IP:str
PORT:int

app = Flask(__name__)

@app.route('/')
def create_app():
    pass

@app.route('/waiting')
def wait():
    return render_template('/transfer/wait.html')