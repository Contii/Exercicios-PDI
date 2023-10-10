import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from vectorOfMats import VectorOfMats

vec_of_mats = VectorOfMats()
vec_of_mats2 = VectorOfMats()   # Crie uma nova instância para armazenar imagens temporariamente


# Função para carregar uma imagem
def carregar_imagem():
    file_path = filedialog.askopenfilename(initialdir="./Media", title="Selecionar uma imagem", filetypes=(("Image files", "*.png *.jpg"), ("All files", "*.*")))
    if file_path:
        print("Imagem selecionada:", file_path)
        vec_of_mats.add_image(file_path)
        # Carregue a imagem usando Pillow (PIL)
        image = Image.open(file_path)
        # Redimensione a imagem para caber na janela com 20 pixels de borda
        image = image.resize((frame_direito.winfo_width() - 40, frame_direito.winfo_height() - 40))
        # Crie um objeto ImageTk para exibir a imagem no Label
        image_tk = ImageTk.PhotoImage(image=image)
        # Atualize a imagem no Label
        label_imagem.configure(image=image_tk)
        label_imagem.image = image_tk  # Mantenha uma referência para evitar que a imagem seja coletada pelo garbage collector

def salvar_imagem():
    if label_imagem.image:  # Verifique se há uma imagem atualmente exibida
        imagem_atual = ImageTk.getimage(label_imagem.image)  # Obtenha a imagem exibida
        if imagem_atual:
            # Converta a imagem para o modo RGB antes de salvar
            imagem_atual_rgb = imagem_atual.convert("RGB")
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=(("JPEG files", "*.jpg"), ("All files", "*.*")))
            if file_path:
                imagem_atual_rgb.save(file_path)
                print("Imagem atual salva em:", file_path)

def exibir_imagem_anterior():
    if len(vec_of_mats.images) > 1:  # Verifique se há pelo menos duas imagens no vetor
        # Remova a imagem atual do vetor e adicione a imagem removida em vec_of_mats2
        imagem_anterior = vec_of_mats.images.pop()
        vec_of_mats2.images.append(imagem_anterior)
        # Obtenha a imagem anterior
        imagem_anterior = vec_of_mats.images[-1]
        # Atualize a imagem exibida na janela com a imagem anterior
        atualizar_imagem_exibida(imagem_anterior)

def exibir_proxima_imagem():
    if len(vec_of_mats2.images) > 0:  # Verifique se há imagens em vec_of_mats2
        # Remova a imagem mais recente de vec_of_mats2 e adicione-a de volta a vec_of_mats
        imagem_proxima = vec_of_mats2.images.pop()
        vec_of_mats.images.append(imagem_proxima)
        # Atualize a imagem exibida na janela com a imagem recuperada
        atualizar_imagem_exibida(imagem_proxima)

def delete_imagem():
    if len(vec_of_mats.images) > 0:
        # Remova a imagem atual do vetor
        vec_of_mats.images.pop()
        # Verifique se ainda há imagens no vetor
        if len(vec_of_mats.images) > 0:
            # Obtenha a imagem anterior
            imagem_anterior = vec_of_mats.images[-1]
            # Atualize a imagem exibida na janela com a imagem anterior
            atualizar_imagem_exibida(imagem_anterior)
        else:
            # Se não houver mais imagens no vetor, limpe a imagem exibida
            label_imagem.configure(image=None)

def atualizar_imagem_exibida(imagem):
    # Converta a imagem de BGR para RGB
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    # Atualize a imagem exibida na janela com a imagem RGB
    imagem_pil = Image.fromarray(imagem_rgb)
    imagem_pil = imagem_pil.resize((frame_direito.winfo_width() - 40, frame_direito.winfo_height() - 40))
    image_tk = ImageTk.PhotoImage(image=imagem_pil)
    label_imagem.configure(image=image_tk)
    label_imagem.image = image_tk

# Variável global para armazenar o valor da trackbar
threshold_value = 128

def converter_cor(imagem):
    # Aplicar a conversão de cor na imagem (por exemplo, converter para tons de cinza)
    imagem_convertida = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    # Converta a imagem de BGR para RGB antes de armazenar no vetor
    imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
    return imagem_convertida_rgb
def aplicar_conversao_cor():
    if vec_of_mats.images:
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = converter_cor(imagem_original)  # Aplique a conversão de cor
        vec_of_mats.images.append(imagem_convertida)  # Armazene a imagem convertida no vetor
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Imagem convertida e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)

# Função para aplicar a conversão de cor em tempo real
def aplicar_conversao_cor_em_tempo_real(value):
    global threshold_value
    threshold_value = value
    imagem_original = vec_of_mats.images[-1]
    imagem_convertida = converter_cor(imagem_original)
    vec_of_mats.images.append(imagem_convertida)
    atualizar_imagem_exibida(imagem_convertida)

# Função para aplicar a conversão de cor
def aplicar_conversao_cor():
    # Crie uma janela para ajustar a conversão em tempo real
    janela_ajuste = tk.Toplevel()
    janela_ajuste.title("Ajuste de Conversão de Cor")

    # Crie uma trackbar para ajustar o valor da conversão em tempo real
    trackbar = tk.Scale(janela_ajuste, from_=0, to=255, orient="horizontal", label="Valor de Conversão",
                        command=aplicar_conversao_cor_em_tempo_real)
    trackbar.set(threshold_value)  # Defina o valor inicial da trackbar
    trackbar.pack(padx=10, pady=10)


def apply_filter(imagem):
    imagem_convertida_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
    # Aplique o filtro à imagem atual, você pode aplicar um filtro de suavização da seguinte forma:
    imagem_convertida = cv2.GaussianBlur(imagem_convertida_bgr, (5, 5), 0)
    # Converta a imagem de BGR para RGB antes de armazenar no vetor
    imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
    return imagem_convertida_rgb
def aplicar_filtro():
    if vec_of_mats.images:
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = apply_filter(imagem_original)  # Aplique a conversão de cor
        vec_of_mats.images.append(imagem_convertida)  # Armazene a imagem convertida no vetor
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Aplicado o filtro e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)


def aplicar_detecao(imagem):
    # Aplique a detecção de bordas usando o operador Canny
    imagem_convertida = cv2.Canny(imagem, 100, 200)
    # Converta a imagem de BGR para RGB antes de armazenar no vetor
    imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
    return imagem_convertida_rgb
def detectar_bordas():
    if vec_of_mats.images:
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = aplicar_detecao(imagem_original) # Você pode ajustar os valores 100 e 200 conforme necessário
        vec_of_mats.images.append(imagem_convertida)
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Imagem com bordas detectadas e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)


def aplicar_binarizacao(imagem):
     # Converta a imagem para tons de cinza (se já não estiver em tons de cinza)
        if len(imagem.shape) == 3:
            imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        # Aplique a binarização da imagem
        _, imagem_convertida = cv2.threshold(imagem, 128, 255, cv2.THRESH_BINARY)
        # Converta a imagem de BGR para RGB antes de armazenar no vetor
        imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
        return imagem_convertida_rgb
def binarizar_imagem():
    if vec_of_mats.images:
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = aplicar_binarizacao(imagem_original) # Você pode ajustar os valores 100 e 200 conforme necessário
        vec_of_mats.images.append(imagem_convertida)
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Imagem binarizada e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)


def apply_morphology(imagem):
        # Certifique-se de que a imagem está binarizada (use o valor adequado de limiar)
        _, imagem_binaria = cv2.threshold(imagem, 128, 255, cv2.THRESH_BINARY)
        # Defina o kernel para a operação de erosão (pode ajustar o tamanho do kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # Aplique a operação de erosão
        imagem_convertida = cv2.erode(imagem_binaria, kernel, iterations=1)
        # Converta a imagem de BGR para RGB antes de armazenar no vetor
        imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
        return imagem_convertida_rgb
def aplicar_morfologia():
    if vec_of_mats.images:
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = apply_morphology(imagem_original) # Você pode ajustar os valores 100 e 200 conforme necessário
        vec_of_mats.images.append(imagem_convertida)
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Aplicada a morfologia e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)



# Crie a janela principal
janela = tk.Tk()
janela.title("Minha Janela")
janela.geometry("800x600")
# Divida a janela em 2 colunas e 1 linha
janela.grid_rowconfigure(0, weight=1)
janela.columnconfigure(0, weight=1)
janela.columnconfigure(1, weight=4)



# Parte esquerda (20% da largura)
frame_esquerdo = tk.Frame(janela, bg="light gray")
frame_esquerdo.grid(row=0, column=0, sticky="nsew")  # "nsew" para preencher na direção norte-sul-leste-oeste

largura_botoes = 15
# Adicione seus botões ao frame_esquerdo
botao1 = tk.Button(frame_esquerdo, text="Carregar imagem", width=largura_botoes, command=carregar_imagem)
botao1.grid(row=0, column=0, padx=10, pady=(10,40))
botao2 = tk.Button(frame_esquerdo, text="convert_color", width=largura_botoes, command=aplicar_conversao_cor)
botao2.grid(row=1, column=0, padx=10, pady=10)
botao3 = tk.Button(frame_esquerdo, text="apply_filter", width=largura_botoes, command=aplicar_filtro)
botao3.grid(row=2, column=0, padx=10, pady=10)
botao4 = tk.Button(frame_esquerdo, text="detect_edges", width=largura_botoes, command=detectar_bordas)
botao4.grid(row=3, column=0, padx=10, pady=10)
botao5 = tk.Button(frame_esquerdo, text="binarize", width=largura_botoes, command=binarizar_imagem)
botao5.grid(row=4, column=0, padx=10, pady=10)
botao6 = tk.Button(frame_esquerdo, text="apply_morphology", width=largura_botoes, command=aplicar_morfologia)
botao6.grid(row=5, column=0, padx=10, pady=(10, 40))
botao_salvar = tk.Button(frame_esquerdo, text="Salvar Imagem", width=largura_botoes, command=salvar_imagem)
botao_salvar.grid(row=6, column=0, padx=10, pady=10)
# Crie um novo Frame dentro do frame esquerdo para os botões "Next" e "Previous"
frame_botoes_nav = tk.Frame(frame_esquerdo, bg="light gray")
frame_botoes_nav.grid(row=7, column=0, padx=10, pady=10)
# Configure os botões "Next" e "Previous"
botao_previous = tk.Button(frame_botoes_nav, text="  <  ", width=5, command=exibir_imagem_anterior)
botao_previous.pack(side="left", padx=5)
botao_next = tk.Button(frame_botoes_nav, text="  >  ", width=5, command=exibir_proxima_imagem)
botao_next.pack(side="left", padx=5)
botao_delete = tk.Button(frame_esquerdo, text="  X  ", width=5, command=delete_imagem)
botao_delete.grid(row=8, column=0, padx=10, pady=10)


# Parte direita (80% da largura)
frame_direito = tk.Frame(janela, bg="white")
frame_direito.grid(row=0, column=1, sticky="nsew")
# Crie um novo Frame dentro do frame_direito para a imagem
frame_imagem = tk.Frame(frame_direito)
frame_imagem.pack(fill="both", expand=True)
# Crie um Label para exibir a imagem
label_imagem = tk.Label(frame_imagem)
label_imagem.pack(fill="both", expand=True)



# Função para fechar a janela
def fechar_janela():
    janela.destroy()
# Configure o botão para fechar a janela
janela.protocol("WM_DELETE_WINDOW", fechar_janela)
# Use o weight para que as colunas se expandam com o redimensionamento da janela
janela.mainloop()