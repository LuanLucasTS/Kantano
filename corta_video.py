import cv2

video_path = "static/video/kda.mp4"
output_path = "static/video/cortado.mp4"

cap = cv2.VideoCapture(video_path)

# Obter informações do vídeo
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Inicializar o codificador de vídeo
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Definir o intervalo de tempo que deseja cortar
start_time = 30 # segundos
duration = 15 # segundos

# Avançar para o começo do intervalo de tempo que deseja cortar
cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

# Lêr o vídeo frame a frame e escreve os frames no novo vídeo
frame_counter = 0
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    out.write(frame)
    frame_counter += 1

    if frame_counter >= fps * duration:
        break

# Limpar recursos
cap.release()
out.release()