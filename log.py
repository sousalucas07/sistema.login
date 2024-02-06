import requests

def cadastro_usuario_interface():
    print("Bem-vindo ao sistema de cadastro!")
    nome = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    confirm_password = input("Confirme sua senha: ")

    if senha == confirm_password:
        data = {'nome': nome, 'senha': senha, 'confirm_password': confirm_password}
        response = requests.post('http://127.0.0.1:5000/registrar', json=data)

        if response.status_code == 201:
            print("Usuário registrado com sucesso!")
        else:
            print("Erro ao registrar usuário:", response.json()['error'])
    else:
        print("As senhas não coincidem.")

if __name__ == "__main__":
    cadastro_usuario_interface()

