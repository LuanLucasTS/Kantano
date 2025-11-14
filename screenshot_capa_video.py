import cv2

# Carregar o vídeo
video = cv2.VideoCapture("static/video/kda.mp4")

# Ir para a posição de tempo desejada (em segundos)
time = 30
video.set(cv2.CAP_PROP_POS_MSEC, time * 1000)

# Ler o frame no tempo especificado
success, image = video.read()

# Verificar se a imagem foi lida com sucesso
if success:
    # Salvar a imagem
    cv2.imwrite("screenshot.png", image)

# Liberar o objeto de vídeo
video.release()