
from flask import Flask, request, jsonify, send_from_directory, render_template
import mysql.connector
import bcrypt
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

conn = {
    'host': 'localhost',
    'user': 'root',
    'password': '2706Lps@',
    'database': 'LOGIN'
}

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        # Conectar ao banco de dados
        conexao = mysql.connector.connect(
            host=conn['host'],
            user=conn['user'],
            password=conn['password'],
            database=conn['database'])
        print("Conexão bem-sucedida ao banco de dados!")
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None

# Função para registrar novos usuários no banco de dados
@app.route('/registrar', methods=['POST'])
def registro_usuario():
    data = request.get_json()
    nome = data['nome']
    senha = data['senha']
    confirm_password = data['confirm_password']

    if senha == confirm_password:
        conexao = conectar_banco()
        if conexao is not None:
            try:
                hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (nome, hashed_password))
                conexao.commit()
                conexao.close()
                return jsonify({'message': 'Usuário registrado com sucesso!'}), 201
            except mysql.connector.Error as erro:
                return jsonify({'error': f"Erro ao registrar usuário: {erro}"}), 500
    else:
        return jsonify({'error': 'As senhas não coincidem.'}), 400

# Função para autenticar usuários e gerar token JWT
@app.route('/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    nome = data['nome']
    senha = data['senha']

    conexao = conectar_banco()
    if conexao is not None:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
            usuario = cursor.fetchone()
            if usuario:
                if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
                    payload = {
                        'nome': usuario['nome'],
                        'exp': datetime.utcnow() + timedelta(hours=1)
                    }
                    jwt_token = jwt.encode(payload, 'chave_secreta', algorithm='HS256')
                    conexao.close()
                    return jsonify({'token': jwt_token.decode('utf-8')}), 200
                else:
                    return jsonify({'error': 'Senha incorreta.'}), 401
            else:
                return jsonify({'error': 'Usuário não encontrado.'}), 404
        except mysql.connector.Error as erro:
            return jsonify({'error': f"Erro ao autenticar usuário: {erro}"}), 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

