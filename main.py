#pip3 install flask
#pip3 install spotipy

from flask import Flask, render_template, request, redirect, url_for
from helpers import get_db_connection, gerar_legendas, baixar_informacoes_spotify
from datetime import date
import urllib.request
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kantano'

conn = get_db_connection()

@app.route('/')
def home():
    musicas = conn.execute("SELECT * FROM musicas order by titulo").fetchall()
    pagina = conn.execute("SELECT * FROM paginas where nome='todas'").fetchall()
    return render_template('genero.html', musicas=musicas, pagina=pagina)

@app.route('/kpop')
def kpop():
    musicas = conn.execute("SELECT * FROM musicas where genero like 'k-pop' or genero like '%kpop%'order by titulo").fetchall()
    pagina = conn.execute("SELECT * FROM paginas where nome='kpop'").fetchall()
    return render_template('genero.html', musicas=musicas, pagina=pagina)

@app.route('/pop')
def pop():
    musicas = conn.execute("SELECT * FROM musicas where genero like 'dance pop'order by titulo").fetchall()
    pagina = conn.execute("SELECT * FROM paginas where nome='pop'").fetchall()
    return render_template('genero.html', musicas=musicas, pagina=pagina)

@app.route('/rock')
def rock():
    musicas = conn.execute("SELECT * FROM musicas where genero like '%rock%'or genero like '%metal%' order by titulo").fetchall()
    pagina = conn.execute("SELECT * FROM paginas where nome='rock'").fetchall()
    return render_template('genero.html', musicas=musicas, pagina=pagina)

@app.route('/anime')
def anime():
    musicas = conn.execute("SELECT * FROM musicas where genero like '%anime%' order by titulo").fetchall()
    pagina = conn.execute("SELECT * FROM paginas where nome='anime'").fetchall()
    return render_template('genero.html', musicas=musicas, pagina=pagina)

@app.route('/pesquisa', methods=["GET", "POST"])
def pesquisa():
    if request.method == "POST":
        pesquisa = request.form['pesquisa']
        musicas = conn.execute(f"SELECT * FROM musicas where titulo like '%{pesquisa}%' or artista like '%{pesquisa}%' order by titulo").fetchall()
        pagina = conn.execute("SELECT * FROM paginas where nome='pesquisa'").fetchall()
        return render_template('genero.html', musicas=musicas, pagina=pagina)
    else:
        return redirect(url_for("home"))

@app.route('/random')
def random():
    musicas = conn.execute("SELECT * FROM musicas ORDER BY RANDOM() LIMIT 1").fetchall()
    pagina = conn.execute("SELECT * FROM paginas where nome='random'").fetchall()
    return render_template('genero.html', musicas=musicas, pagina=pagina)

@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/video/<int:id>')
def video(id):
    musica = conn.execute(f"SELECT * FROM musicas where id={id}").fetchall()
    musica2 = (musica[0]['capa'])
    musica2 = musica2.replace('.jpg', '')
    print(musica2)
    legenda = conn.execute(f"SELECT inicio, fim, parametro, atual, proxima FROM legendas where musica='{musica2}'").fetchall()
    with open(f'static/legenda/{musica2}.vtt', 'w', encoding="utf-8") as f:
        vtt = "WEBVTT\n"
        f.write(str(vtt))
        for linha in legenda:
            texto = '\n{} --> {} {}\n<b>{}</b>\n{}\n'.format(*linha)
            texto = texto.replace("\r", "")
            f.write(str(texto) )

    return render_template('video.html', musica=musica, musica2=musica2)

@app.route('/adicionar_musica', methods=["GET", "POST"])
def adicionar_musica():
    if request.method == "POST":
        data_atual = date.today()
        data_alteracao= data_atual
        video = request.files['video']
        titulo = request.form['titulo']
        artista = request.form['artista']
        spotify = baixar_informacoes_spotify(titulo, artista)
        capa = f'{spotify[0]}-{spotify[1]}.jpg'
        nomevideo = f'{spotify[0]}-{spotify[1]}.mp4'
        musica = f'{spotify[0]}-{spotify[1]}'
        legenda = request.form['legenda']
        legenda = legenda.replace("\n", "")
        legenda = legenda.replace("'", "")
        with open('legenda.txt', 'w', encoding='utf-8') as f:
            f.write(legenda)
        gerar_legendas(musica)
        conn.execute('INSERT INTO musicas (titulo, artista, genero, capa, datainsercao, dataalteracao, album, video) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (spotify[0], spotify[1], spotify[3], capa, data_atual, data_alteracao, spotify[2], nomevideo))
        video.save(f'static/video/{spotify[0]}-{spotify[1]}.mp4')
        conn.commit()
        return redirect(url_for("adicionar_musica"))
    else:
        pagina = conn.execute("SELECT * FROM paginas where nome='adicionar'").fetchall()
        return render_template('adicionar_musica.html', pagina=pagina)


@app.route('/editar_legendas', methods=["GET", "POST"])
def editar_legendas():
    musicas = conn.execute("SELECT * FROM musicas").fetchall()
    pagina = conn.execute("SELECT * FROM paginas where nome='editar_legendas'").fetchall()
    return render_template("editar_legendas.html", musicas=musicas, pagina=pagina)


@app.route('/legenda/<int:id>', methods=["GET", "POST"])
def legenda(id):
    if request.method == "GET":
        pagina = conn.execute("SELECT * FROM paginas where nome='editar_legendas'").fetchall()
        musica = conn.execute(f"SELECT titulo, artista FROM musicas where id={id}").fetchone()
        musica = f'{musica[0]}-{musica[1]}'
        idmusica = id
        legenda = conn.execute(f"SELECT * FROM legendas where musica='{musica}'").fetchall()
        return render_template("legenda.html", legenda=legenda, pagina=pagina, musica=musica, idmusica=idmusica)
    else:
        id = request.form['id']
        inicio = request.form['inicio']
        fim = request.form['fim']
        atual = request.form['atual']
        proxima = request.form['proxima']
        idmusica = request.form['idmusica']
        alterado = date.today()
        conn.execute(f"update legendas set inicio='{inicio}', fim='{fim}', atual='{atual}', proxima='{proxima}', dataalteracao='{alterado}' where id={id}")
        conn.commit()
        return redirect(url_for("legenda", id=idmusica))



@app.route('/editar_musicas', methods=["GET", "POST"])
def editar_musicas():
    if request.method == "GET":
        musicas = conn.execute("SELECT * FROM musicas").fetchall()
        pagina = conn.execute("SELECT * FROM paginas where nome='editar_musicas'").fetchall()
        return render_template("editar_musicas.html", musicas=musicas, pagina=pagina)
    else:
        id = request.form['id']
        titulo = request.form['titulo']
        artista = request.form['artista']
        genero = request.form['genero']
        album = request.form['album']
        alterado = date.today()
        conn.execute(f"update musicas set titulo='{titulo}', artista='{artista}', genero='{genero}', album='{album}', video='{video}', dataalteracao='{alterado}' where id={id}")
        conn.commit()
        return redirect(url_for("editar_musicas"))

@app.route('/alterar_capa/<string:capa>', methods=["GET", "POST"])
def alterar_capa(capa):
    pagina = conn.execute("SELECT * FROM paginas where nome='editar_capa'").fetchall()
    if request.method == "GET":
        return render_template("alterar_capa.html", pagina=pagina, capa=capa)
    else:
        url = request.form['url']
        capa = request.form['capa']
        arquivo = request.files['arquivo']
        if url == '':
            arquivo.save(f'static/imagens/capas/{capa}')
        else:
            urllib.request.urlretrieve(f'{url}',f'static/imagens/capas/{capa}')
        return redirect(url_for("alterar_capa", pagina=pagina, capa=capa))

@app.route('/alterar_video/<string:video>', methods=["GET", "POST"])
def alterar_video(video):
    pagina = conn.execute("SELECT * FROM paginas where nome='editar_video'").fetchall()
    if request.method == "GET":
        return render_template("alterar_video.html", pagina=pagina, video=video)
    else:
        video = request.form['video']
        arquivo = request.files['arquivo']
        if not arquivo:
            return redirect(url_for("alterar_video", pagina=pagina, video=video))
        else:
            arquivo.save(f'static/video/{video}')
        return redirect(url_for("alterar_video", pagina=pagina, video=video))


@app.route('/deletar_musica/<int:id>')
def deletar_musica(id):
    musica = conn.execute(f"SELECT * FROM musicas where id={id}").fetchone()
    capa = musica[4]
    video = musica[8]
    letra = f'{musica[1]}-{musica[2]}'
    os.remove(f'static/imagens/capas/{capa}')
    os.remove(f'static/video/{video}')
    conn.execute(f"delete from legendas where musica='{letra}'")
    conn.execute(f"delete from musicas where id={id}")
    conn.commit()
    return redirect(url_for("editar_musicas"))

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
