import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# Defina as suas credenciais de acesso aqui
client_id = 'key'
client_secret = 'key'

# Crie uma instância do objeto de autenticação do Spotify
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Busque uma música pelo título e artista
results = sp.search(q='K/DA MORE', type='track')

# Imprima o título, artista e álbum da primeira música encontrada
track = results['tracks']['items'][0]
artist_info = sp.artist(track['artists'][0]['id'])

print("Título: ", track['name'])
print("Artista: ", track['artists'][0]['name'])
print("Álbum: ", track['album']['name'])
print("Genero: ", artist_info['genres'][0])

# Imprima a URL da capa da música
print("Capa: ", track['album']['images'][0]['url'])

# Obtenha a URL da capa da música
image_url = track['album']['images'][0]['url']

# Baixe a imagem a partir da URL
response = requests.get(image_url)

# Salve a imagem em um arquivo local
with open(f'static/imagens/capascover.jpg', 'wb') as f:
    f.write(response.content)