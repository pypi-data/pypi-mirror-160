import requests


def buscar_avatar(nome_do_usuario):
    """
    busca o avatar de um usuario do github
    :param nome_do_usuario: str com nome de usuario do github
    :return: str com link do avatar
    """
    url = f'https://api.github.com/users/{nome_do_usuario}'
    resposta = requests.get(url)
    return resposta.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('gustavossandrin'))
