import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import random

# Função para aplicar o filtro gaussiano
def aplicar_filtro():
    valor_atual = filtro_value.get()
    imagem_filtrada = apply_gaussian_filter(imagem_original, valor_atual)
    atualizar_imagem_exibida(imagem_filtrada)
    botao_aplicar_filtro.config(state="disabled")
    botao_confirmar_filtro.config(state="normal")

def confirmar_filtro():
    botao_aplicar_filtro.config(state="normal")
    botao_confirmar_filtro.config(state="disabled")

# Função para aplicar o filtro gaussiano
def apply_gaussian_filter(imagem, valor):
    imagem_convertida_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
    imagem_filtrada = cv2.GaussianBlur(imagem_convertida_bgr, (5, 5), valor)
    imagem_filtrada_rgb = cv2.cvtColor(imagem_filtrada, cv2.COLOR_BGR2RGB)
    return imagem_filtrada_rgb

# Função para atualizar a imagem exibida na janela
def atualizar_imagem_exibida(imagem):
    imagem_pil = Image.fromarray(imagem)
    imagem_pil = imagem_pil.resize((800, 600))
    image_tk = ImageTk.PhotoImage(image=imagem_pil)
    label_imagem.configure(image=image_tk)
    label_imagem.image = image_tk

# Função para carregar uma imagem aleatória da pasta "Media"
def carregar_imagem_aleatoria():
    imagem_path = random.choice(["./Media/lenna.jpg", "./Media/bocha.jpg"])
    imagem = cv2.imread(imagem_path)
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    atualizar_imagem_exibida(imagem_rgb)
    global imagem_original
    imagem_original = imagem_rgb

# Crie a janela
janela = tk.Tk()
janela.title("Aplicação de Filtro")
janela.geometry("800x600")

# Crie um label para exibir a imagem
label_imagem = tk.Label(janela)
label_imagem.pack(expand=True, fill="both")

# Crie uma escala (barra de rolagem) para ajustar o filtro
filtro_value = tk.DoubleVar()
scale_filtro = tk.Scale(janela, from_=0, to=10, orient="horizontal", variable=filtro_value, label="Intensidade do Filtro")
scale_filtro.pack()

# Crie um botão para aplicar o filtro
botao_aplicar_filtro = tk.Button(janela, text="Aplicar Filtro", command=aplicar_filtro)
botao_aplicar_filtro.pack()

# Crie um botão para confirmar o filtro
botao_confirmar_filtro = tk.Button(janela, text="Confirmar Filtro", command=confirmar_filtro, state="disabled")
botao_confirmar_filtro.pack()

# Crie um botão para carregar uma imagem aleatória
botao_carregar_imagem = tk.Button(janela, text="Carregar Imagem Aleatória", command=carregar_imagem_aleatoria)
botao_carregar_imagem.pack()

janela.mainloop()