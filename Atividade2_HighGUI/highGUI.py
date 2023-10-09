import cv2
import os
import random
import numpy as np

# Obtém o caminho para a pasta "Media" a partir da raiz do projeto
media_folder = os.path.join(os.path.dirname(__file__), "../Media")

# Lista de vídeos na pasta "Media"
videos = os.listdir(media_folder)
videos = [video for video in videos if video.endswith(".mp4")]

# Variáveis globais para os parâmetros dos filtros
filtro1_valor = 0
filtro2_valor = 0

def binarizar_com_media(imagem):
    # Converte a imagem para escala de cinza
    imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
    # Calcula a média das intensidades dos pixels
    media = cv2.mean(imagem_gray)[0]
    
    # Binariza a imagem usando a média como limiar
    _, imagem_bin = cv2.threshold(imagem_gray, media, 255, cv2.THRESH_BINARY)
    
    return imagem_bin

# Função para aplicar filtros passa-baixa
def aplicar_filtro(frame, filtro1, filtro2):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    filtro1 = cv2.GaussianBlur(frame_gray, (filtro1 * 2 + 1, filtro1 * 2 + 1), 0)
    
    # Garanta que filtro2 seja ímpar e esteja dentro dos limites adequados
    filtro2 = max(1, filtro2 // 2 * 2 + 1)  # Torna filtro2 ímpar e pelo menos 1
    
    filtro2 = cv2.medianBlur(frame_gray, filtro2)
    
    frame_filtrado = cv2.merge([frame_gray, filtro1, filtro2])
    return frame_filtrado


# Função para aplicar o filtro GaussianBlur em R e G
def aplicar_filtro_rgb(frame, filtro1, filtro2):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Aplica o filtro GaussianBlur apenas no canal R (vermelho) da imagem
    frame_rgb[:, :, 0] = cv2.GaussianBlur(frame_rgb[:, :, 0], (filtro1 * 2 + 1, filtro1 * 2 + 1), 0)

    # Aplica o filtro GaussianBlur apenas no canal G (verde) da imagem
    frame_rgb[:, :, 1] = cv2.GaussianBlur(frame_rgb[:, :, 1], (filtro2 * 2 + 1, filtro2 * 2 + 1), 0)
    
    return cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)


# Função para aplicar o filtro passa-alta (Laplaciano) na imagem RGB
def aplicar_filtro_laplaciano(frame, filtro1):
    # Converte a imagem para o espaço de cores BGR2RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Aplica o filtro Laplaciano com o valor do filtro1
    frame_laplaciano = cv2.Laplacian(frame_rgb, cv2.CV_64F, ksize=5)
    
    # Escala os valores resultantes para o intervalo 0-255
    frame_laplaciano = cv2.convertScaleAbs(frame_laplaciano)
    
    # Mescla o resultado com a imagem original
    frame_filtrado = cv2.addWeighted(frame_rgb, 1, frame_laplaciano, filtro1 / 100, 0)
    
    return cv2.cvtColor(frame_filtrado, cv2.COLOR_RGB2BGR)



# Função para reproduzir um vídeo aleatório
def play_random_video():
    global filtro1_valor, filtro2_valor
    
    # Seleciona um vídeo aleatório
    video = random.choice(videos)

    while True:
        # Abre o vídeo
        video_path = os.path.join(media_folder, video)
        video_capture = cv2.VideoCapture(video_path)

        # Cria uma janela para exibir o vídeo original
        cv2.namedWindow("Vídeo original", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Vídeo original", 480, 854)

        # Exibe o vídeo original
        while True:
            # Lê um quadro do vídeo
            ret, frame = video_capture.read()

            # Verifica se o vídeo terminou
            if not ret:
                # O vídeo acabou, então reinicia
                video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                # Lê o próximo quadro após reiniciar
                ret, frame = video_capture.read()

                # Se não houver mais quadros, saia do loop
                if not ret:
                    break

            # Exibe o quadro na janela
            cv2.imshow("Vídeo original", frame)

            # Espera pelo usuário pressionar qualquer tecla
            key = cv2.waitKey(1)

            # Sai do loop do vídeo se o usuário pressionar a tecla ESC
            if key == 27:
                break

            # Abre uma nova janela com o frame capturado do mesmo tamanho
            if key == ord("1"):
                new_window = cv2.namedWindow("Frame capturado", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Frame capturado", 480, 854+82)
                cv2.imshow("Frame capturado", frame)

                # Define o manipulador de eventos de clique do mouse para a nova janela
                cv2.setMouseCallback("Frame capturado", on_mouse_click, frame)

                # Cria os trackbars na segunda janela
                cv2.createTrackbar("Filtro 1", "Frame capturado", 0, 500, lambda x: None)
                cv2.createTrackbar("Filtro 2", "Frame capturado", 0, 500, lambda x: None)

                key = cv2.waitKey(1)


                # Exibe o quadro na segunda janela
                while True:
                    # Obtém o valor da trackbar
                    filtro1_valor = cv2.getTrackbarPos("Filtro 1", "Frame capturado")
                    filtro2_valor = cv2.getTrackbarPos("Filtro 2", "Frame capturado")


                    frame_filtrado = aplicar_filtro_rgb(frame.copy(), filtro1_valor, filtro2_valor)
                    cv2.imshow("Frame capturado", frame_filtrado)

                    # Espera pelo usuário pressionar qualquer tecla
                    key = cv2.waitKey(1)
                    
                    # Sai do loop da segunda janela se o usuário pressionar a tecla ESC
                    if key == 27:
                        break
                    
                    if key == ord("4"):
                        frame_binario = binarizar_com_media(frame_filtrado)  # Substitua 'limiar' pelo valor desejado
                        # Realiza a binarização da imagem
                        cv2.namedWindow("Frame capturado Binario", cv2.WINDOW_NORMAL)
                        cv2.resizeWindow("Frame capturado Binario", 480, 854+82)

                        # Exibe a imagem binarizada em uma nova janela
                        cv2.imshow("Frame capturado Binario", frame_binario)
                         # Espera pelo usuário pressionar qualquer tecla
                        key = cv2.waitKey(1)
                    
                        # Sai do loop da segunda janela se o usuário pressionar a tecla ESC
                        if key == 27:
                            break

                cv2.destroyWindow("Frame capturado")
            
            # Abre uma nova janela com o frame capturado do mesmo tamanho
            if key == ord("2"):
                new_window = cv2.namedWindow("Frame capturado", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Frame capturado", 480, 854+82)
                cv2.imshow("Frame capturado", frame)

                # Define o manipulador de eventos de clique do mouse para a nova janela
                cv2.setMouseCallback("Frame capturado", on_mouse_click, frame)

                # Cria os trackbars na segunda janela
                cv2.createTrackbar("Filtro GaussianBlur", "Frame capturado", 0, 500, lambda x: None)
                cv2.createTrackbar("Filtro MedianBlur", "Frame capturado", 0, 500, lambda x: None)

                key = cv2.waitKey(1)

                # Exibe o quadro na segunda janela
                while True:
                    # Obtém os valores dos trackbars
                    filtro1_valor = cv2.getTrackbarPos("Filtro GaussianBlur", "Frame capturado")
                    filtro2_valor = cv2.getTrackbarPos("Filtro MedianBlur", "Frame capturado")

                    frame_filtrado = aplicar_filtro(frame.copy(), filtro1_valor, filtro2_valor)
                    cv2.imshow("Frame capturado", frame_filtrado)

                    # Espera pelo usuário pressionar qualquer tecla
                    key = cv2.waitKey(1)

                    # Sai do loop da segunda janela se o usuário pressionar a tecla ESC
                    if key == 27:
                        break

                    if key == ord("4"):
                        frame_binario = binarizar_com_media(frame_filtrado)  # Substitua 'limiar' pelo valor desejado
                        # Realiza a binarização da imagem
                        cv2.namedWindow("Frame capturado Binario", cv2.WINDOW_NORMAL)
                        cv2.resizeWindow("Frame capturado Binario", 480, 854+82)

                        # Exibe a imagem binarizada em uma nova janela
                        cv2.imshow("Frame capturado Binario", frame_binario)
                         # Espera pelo usuário pressionar qualquer tecla
                        key = cv2.waitKey(1)
                    
                        # Sai do loop da segunda janela se o usuário pressionar a tecla ESC
                        if key == 27:
                            break


                cv2.destroyWindow("Frame capturado")

            
            # Abre uma nova janela com o frame capturado do mesmo tamanho
            if key == ord("3"):
                new_window = cv2.namedWindow("Frame capturado", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Frame capturado", 480, 854+82)
                cv2.imshow("Frame capturado", frame)

                # Define o manipulador de eventos de clique do mouse para a nova janela
                cv2.setMouseCallback("Frame capturado", on_mouse_click, frame)

                # Cria os trackbars na segunda janela
                cv2.createTrackbar("Filtro 1", "Frame capturado", 0, 500, lambda x: None)

                key = cv2.waitKey(1)


                # Exibe o quadro na segunda janela
                while True:
                    # Obtém o valor da trackbar
                    filtro1_valor = cv2.getTrackbarPos("Filtro 1", "Frame capturado")


                    frame_filtrado = aplicar_filtro_laplaciano(frame.copy(), filtro1_valor)
                    cv2.imshow("Frame capturado", frame_filtrado)

                    # Espera pelo usuário pressionar qualquer tecla
                    key = cv2.waitKey(1)

                    # Sai do loop da segunda janela se o usuário pressionar a tecla ESC
                    if key == 27:
                        break

                    if key == ord("4"):
                        frame_binario = binarizar_com_media(frame_filtrado)  # Substitua 'limiar' pelo valor desejado
                        # Realiza a binarização da imagem
                        cv2.namedWindow("Frame capturado Binario", cv2.WINDOW_NORMAL)
                        cv2.resizeWindow("Frame capturado Binario", 480, 854+82)

                        # Exibe a imagem binarizada em uma nova janela
                        cv2.imshow("Frame capturado Binario", frame_binario)
                         # Espera pelo usuário pressionar qualquer tecla
                        key = cv2.waitKey(1)
                    
                        # Sai do loop da segunda janela se o usuário pressionar a tecla ESC
                        if key == 27:
                            break

                cv2.destroyWindow("Frame capturado")

        # Fecha a janela do vídeo original
        cv2.destroyWindow("Vídeo original")
        return False
    
# Função para o clique do mouse
def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Verifica se o botão esquerdo do mouse foi pressionado
        frame_filtrado = param  # Obtém o frame filtrado passado como parâmetro
        # Obtém a cor do pixel clicado
        color = frame_filtrado[y, x]

        # Cria uma imagem de 200x200 pixels com a cor do pixel clicado
        color_image = np.zeros((200, 200, 3), dtype=np.uint8)
        color_image[:] = color

        # Abre uma nova janela com a cor correspondente
        cv2.imshow("Cor Clicada", color_image)

def highGUI():
# Menu principal
    while True:
        # Exibe o menu
        os.system('cls')
        print("======= Atividade2-HighGUI =======")
        print("1 - Abrir vídeo aleatório")
        print("3 - Sair")
        print("==============================")


        # Lê a opção do usuário
        option = input("Opção: ")

        # Verifica a opção do usuário
        if option == "1":
            # Reproduz um vídeo aleatório
            print("===========================================================")
            print("Atenção, os filtros podem sobrecarregar sua máquina.")
            print("Pressione 1 para capturar um frame com filtros Passa-Baixa")
            print("Pressione 2 para capturar um frame com filtros Passa-Baixa")
            print("Pressione 3 para capturar um frame com o filta Passa-Alta")
            print("Pressione 4 para binarizar a imagem")
            print("Pressione ESC para sair")

            print("===========================================================")
            play_random_video()
        elif option == "3":
            # Sai do programa
         break

if __name__ == "__highGUI__":
    highGUI()