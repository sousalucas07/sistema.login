from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from registro import registro_usuario_blueprint

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

app.register_blueprint(registro_usuario_blueprint)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
