import youtube_dl

# Crie uma instância do objeto `YoutubeDL`
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

# Defina a URL do vídeo ou áudio que você deseja baixar
url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# Use o método `extract_info` do objeto `YoutubeDL` para baixar as informações
info = ydl.extract_info(url, download=False)

# Imprima o título, autor e duração da música
print("Título: ", info['title'])
print("Autor: ", info['artist'] if 'artist' in info else 'Desconhecido')
print("Duração: ", info['duration'])


# Imprima a URL da capa da música
print("Capa: ", info['thumbnail'])
