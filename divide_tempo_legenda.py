import re

texto = "[00:05.66]You know who it is"

padrao = re.compile(r'\[(\d{2}:\d{2}\.\d{2})\]')
resultado = re.search(padrao, texto)

if resultado:
  tempo = resultado.group(1)
  print(tempo)
else:
  print("Padrão não encontrado.")