from helpers import get_db_connection, arruma_ultimo_tempo
import re
conn = get_db_connection()

with open('letra.txt', 'r', encoding='utf-8') as arquivo:
  linhas = arquivo.readlines()

padrao = re.compile(r'\[(\d{2}:\d{2}\.\d{2})\]')

for linha in linhas:
  resultado = re.search(padrao, linha)

  if resultado:
    tempo = "00:" + resultado.group(1) + "0"
    texto = linha.replace('[' + resultado.group(1) + ']', '').strip()
    conn.execute("INSERT INTO legendas (inicio, atual, musica) VALUES (?, ?, ?)", (tempo, texto, "more"))

conn.commit()

dados = conn.execute("select id, inicio, atual  from legendas where musica='more' order by rowid limit -1 offset 1 ").fetchall()
for dados in dados:
  conn.execute(f"update legendas set fim='{dados[1]}', proxima='{dados[2]}' where musica='more' and id='{dados[0]-1}'")


ultimo_tempo = conn.execute("select inicio from legendas where id=(select max(id)from legendas where musica='more')").fetchone()
ultimo_tempo = arruma_ultimo_tempo(ultimo_tempo[0])
conn.execute(f"update legendas set fim='{ultimo_tempo}' where musica='more' and id=(select max(id)from legendas where musica='more')")
conn.execute(f"update legendas set proxima =' ' WHERE id=(select max(id)from legendas where musica='more')")

conn.commit()
conn.close()