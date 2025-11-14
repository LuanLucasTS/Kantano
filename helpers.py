import sqlite3
import re
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

def get_db_connection():
    conn = sqlite3.connect('banco.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def arruma_ultimo_tempo(ultimo_tempo):
    horas, minutos, segundos_centesimos = map(str, ultimo_tempo.split(":"))
    segundos, centesimos = map(str, segundos_centesimos.split("."))
    segundos_totais = int(segundos) + 10

    if segundos_totais > 59:
        segundos_totais = '05'

    novo_tempo = f"{horas}:{minutos}:{segundos_totais}.{centesimos}"
    return (novo_tempo)

def gerar_legendas(musica):
    conn = get_db_connection()

    with open('legenda.txt', 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    padrao = re.compile(r'\[(\d{2}:\d{2}\.\d{2})\]')

    for linha in linhas:
        resultado = re.search(padrao, linha)

        if resultado:
            tempo = "00:" + resultado.group(1) + "0"
            texto = linha.replace('[' + resultado.group(1) + ']', '').strip()
            data_atual = date.today()
            data_alteracao = data_atual
            conn.execute("INSERT INTO legendas (inicio, atual, parametro, musica, datainsercao, dataalteracao) VALUES (?, ?, ?, ?, ?, ?)", (tempo, texto, 'line:13', musica, data_atual, data_alteracao))

    conn.commit()

    dados = conn.execute(f"select id, inicio, atual  from legendas where musica='{musica}' order by rowid limit -1 offset 1 ").fetchall()
    for dados in dados:
        conn.execute(f"update legendas set fim='{dados[1]}', proxima='{dados[2]}' where musica='{musica}' and id='{dados[0] - 1}'")

    ultimo_tempo = conn.execute(f"select inicio from legendas where id=(select max(id)from legendas where musica='{musica}')").fetchone()
    ultimo_tempo = arruma_ultimo_tempo(ultimo_tempo[0])
    conn.execute(
        f"update legendas set fim='{ultimo_tempo}' where musica='{musica}' and id=(select max(id)from legendas where musica='{musica}')")
    conn.execute(f"update legendas set proxima =' ' WHERE id=(select max(id)from legendas where musica='{musica}')")

    conn.commit()


def baixar_informacoes_spotify(titulo, artista):
    # Defina as suas credenciais de acesso aqui
    client_id = 'key'
    client_secret = 'key'

    # Crie uma instância do objeto de autenticação do Spotify
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Busque uma música pelo título e artista
    results = sp.search(q=f'{artista} {titulo}', type='track')

    # Imprima o título, artista e álbum da primeira música encontrada
    track = results['tracks']['items'][0]
    artist_info = sp.artist(track['artists'][0]['id'])

    titulo = track['name']
    artista =  track['artists'][0]['name']
    album = track['album']['name']
    genero =  artist_info['genres'][0]

    titulo = re.sub(r'[^\w\s]', '', titulo)
    artista = re.sub(r'[^\w\s]', '', artista)
    album = re.sub(r'[^\w\s]', '', album)
    genero = re.sub(r'[^\w\s]', '', genero)


    # Obtenha a URL da capa da música
    image_url = track['album']['images'][0]['url']

    # Baixe a imagem a partir da URL
    response = requests.get(image_url)

    # Salve a imagem em um arquivo local
    with open(f'static/imagens/capas/{titulo}-{artista}.jpg', 'wb') as f:
        f.write(response.content)

    # Imprima a URL da capa da música
    #print("Capa: ", track['album']['images'][0]['url'])


    return (titulo, artista, album, genero)