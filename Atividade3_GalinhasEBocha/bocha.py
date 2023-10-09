import cv2
import os

import numpy as np

# Função para binarizar a imagem em escala de cinza
def binarizar_imagem(imagem_gray, threshold_value):
    _, binary_img = cv2.threshold(imagem_gray, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_img

# Função para callback da trackbar
def on_trackbar(value, imagem, imagem_gray):
    global threshold_value, binary_img
    threshold_value = value
    binary_img = binarizar_imagem(imagem_gray, threshold_value)
    cv2.imshow('Imagem Binarizada em Escala de Cinza', binary_img)
    # Encontre os contornos na imagem binarizada
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
    # Desenha os contornos na imagem original
    imagem_com_contornos = imagem.copy()
    cv2.drawContours(imagem_com_contornos, contours, -1, (0, 255, 0), 2)  # Desenhe os contornos
    cv2.imshow("Imagem com Contornos", imagem_com_contornos)

# Função principal para processamento da imagem da bocha
def bocha():
    # Obtém o caminho para a pasta "Media" a partir da raiz do projeto
    media_folder = os.path.join(os.path.dirname(__file__), "../Media")    
    image_path = os.path.join(media_folder, 'bocha.JPG')
    imagem = cv2.imread(image_path)
    threshold_value = 160
    minDist = 20
    param1 = 50
    param2 = 30
    minRadius = 10
    maxRadius = 50

    while True:
        os.system('cls')
        print("===== Exercicio 1 - Binarizar Bocha. =====")
        print(" Este exercicio esta incompleto.")
        print(" B - Binarizar Imagem.")
        print(" Q - Sair.")
        escolha = input("Escolha uma opção: ")

        if escolha == 'b':
            # Exibe a imagem em escala de cinza
            imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Imagem em Escala de Cinza', imagem_gray)
            
            # Crie uma janela com a imagem binarizada e uma trackbar para ajustar o threshold
            cv2.namedWindow('Imagem Binarizada em Escala de Cinza')
            cv2.createTrackbar('Threshold', 'Imagem Binarizada em Escala de Cinza', threshold_value, 255, lambda value, img_gray=imagem_gray: on_trackbar(value, imagem, img_gray))

            # Inicialize a imagem binarizada com o valor inicial do threshold
            binary_img = binarizar_imagem(imagem_gray, threshold_value)
            cv2.imshow('Imagem Binarizada em Escala de Cinza', binary_img)
            
            # Aguarde ate alguma tecla ser pressionada
            key = cv2.waitKey(0)
        elif escolha == 'q':
            break

        # Aguarde ate alguma tecla ser pressionada
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__bocha__':
    bocha()




    