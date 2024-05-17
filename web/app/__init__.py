from flask import Flask, render_template, url_for, request, session, current_app, redirect, send_file, jsonify
import json
from PIL import Image
from io import BytesIO
import base64
import hashlib
# from ops import RegistrationForm
from ops import StrDatabase, RegistrationForm

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

@app.route('/transfer/result', methods=["GET", "POST"])
def result():
    image_path = "images/sample_image.png"
    if request.method == "POST":
        json_data = request.get_json()
        dict_data = json.loads(json.dumps(json_data))
        
        image_name = dict_data['name']
        image_path = "images/transfer/" + str(image_name)

        image = dict_data['img']
        image = Image.open(BytesIO(base64.b64encode(image)))
        image.save(image_path)
        
    return render_template('/transfer/result.html', image = image_path)

@app.route('/transfer/download/<path:filename>')
def download(filename):
    filename = "static/" + filename
    return send_file(filename,
                     as_attachment=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        pass
    return render_template("/member/register.html")

@app.route('/check_id', methods=['POST'])
def check_id():
    try:
        data = request.get_json()
        user_id = data['user_id']

        result = db.user_select(user_id)
    except:
        result = True
        pass
    
    print(result)
    if result:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})
    
if __name__ == "__main__":
    app.run(debug=True)
    db = StrDatabase()
