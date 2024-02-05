
import bcrypt
import mysql.connector
import jwt
from datetime import datetime, timedelta
import requests

from flask import Flask, request, jsonify

# Crie uma instância do Flask
app = Flask(__name__)

# Defina uma rota e uma função de visualização
@app.route('/')
def hello():
    return 'Hello, World!'

# Execute o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)

conn = {
    'host': 'localhost',
    'user': 'root',  # Correção aqui
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

con = conectar_banco()

# Função para registrar novos usuários no banco de dados
@app.route('/registro', methods=['POST'])
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

# Interface para cadastro de novos usuários
def cadastro_usuario_interface():
    print("Bem-vindo ao sistema de cadastro!")
    nome = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    confirm_password = input("Confirme sua senha: ")

    if senha == confirm_password:
        # Envia os dados para a rota /registro usando a biblioteca requests
        data = {'nome': nome, 'senha': senha, 'confirm_password': confirm_password}
        response = requests.post('http://localhost:5000/registro', json=data)
        
        # Verifica o código de status da resposta
        if response.status_code == 201:
            print("Usuário registrado com sucesso!")
        else:
            print("Erro ao registrar usuário:", response.json()['error'])
    else:
        print("As senhas não coincidem.")

# Exemplo de uso
if __name__ == "__main__":
    cadastro_usuario_interface()