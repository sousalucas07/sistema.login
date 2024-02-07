from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt

app = Flask(__name__)
CORS(app)

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

# Rota para renderizar o formulário de registro
@app.route('/')
def index():
    return render_template('index.html')

# Rota para lidar com o registro de usuários
@app.route('/registrar', methods=['POST'])
def registro_usuario():
    data = request.form
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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
