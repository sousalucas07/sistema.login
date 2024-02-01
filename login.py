import bcrypt
import mysql.connector
import jwt


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