import bcrypt
import mysql.connector
import jwt
from datetime import datetime, timedelta


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
def registrar_usuario(nome, senha):
    conexao = conectar_banco()
    if conexao is not None:
        try:
            # Criptografar a senha
            hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            cursor = conexao.cursor()
            # Inserir usuário e senha criptografada no banco de dados
            cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (nome, hashed_password))
            conexao.commit()
            print("Usuário registrado com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao registrar usuário: {erro}")
        finally:
            conexao.close()

# Função para autenticar usuários e gerar token JWT
def autenticar_usuario(nome, senha):
    conexao = conectar_banco()
    if conexao is not None:
        try:
            cursor = conexao.cursor(dictionary=True)
            # Buscar usuário pelo nome de usuário
            cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
            usuario = cursor.fetchone()
            if usuario:
                # Verificar a senha
                if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
                    # Gerar token JWT
                    payload = {
                        'nome': usuario['nome'],
                        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expira em 1 hora
                    }
                    jwt_token = jwt.encode(payload, 'chave_secreta', algorithm='HS256')
                    return jwt_token
                else:
                    print("Senha incorreta.")
            else:
                print("Usuário não encontrado.")
        except mysql.connector.Error as erro:
            print(f"Erro ao autenticar usuário: {erro}")
        finally:
            conexao.close()

# Interface para cadastro de novos usuários
def cadastro_usuario_interface():
    print("Bem-vindo ao sistema de cadastro!")
    nome = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    confirm_password = input("Confirme sua senha: ")

    if senha == confirm_password:
        registrar_usuario(nome, senha)
    else:
        print("As senhas não coincidem.")

# Exemplo de uso
if __name__ == "__main__":
    cadastro_usuario_interface()