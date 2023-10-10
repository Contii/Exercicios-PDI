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

def desabilitar_Botoes():
    botao2['state'] = 'disabled'
    botao3['state'] = 'disabled'
    botao4['state'] = 'disabled'
    botao5['state'] = 'disabled'
    botao6['state'] = 'disabled'
    botao_salvar['state'] = 'disabled'
    botao_previous['state'] = 'disabled'
    botao_next['state'] = 'disabled'

def habilitar_Botoes():
    botao2['state'] = 'normal'
    botao3['state'] = 'normal'
    botao4['state'] = 'normal'
    botao5['state'] = 'normal'
    botao6['state'] = 'normal'
    botao_salvar['state'] = 'normal'
    botao_previous['state'] = 'normal'
    botao_next['state'] = 'normal'

# variavel para armazenar valor da trackbar em tempo real
trackbar_value = 0
# variavel para armazenar o valor do botao confirmar
botao_Click = False

def botao_Confirmar():
    global botao_Click 
    botao_Click = True



def converter_cor(imagem):
    global trackbar_value, botao_Click
    imagem_convertida_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
    while not botao_Click:
        # Atualize o valor da trackbar (pode ser ajustado)
        trackbar_value = trackbar.get()
        # Certifique-se de que o tamanho do kernel seja ímpar
        if trackbar_value % 2 == 0:
            trackbar_value += 1
            trackbar.set(trackbar_value)
        # Aplique o filtro Gaussian Blur à imagem atual de acordo com o valor da trackbar
        imagem_convertida_gray = cv2.cvtColor(imagem_convertida_bgr, cv2.COLOR_BGR2GRAY)
        # Ajuste a intensidade da conversão de cinza com base no valor da trackbar
        imagem_convertida_gray = cv2.convertScaleAbs(imagem_convertida_gray, alpha=trackbar_value/255.0)
        imagem_convertida_rgb = cv2.cvtColor(imagem_convertida_gray, cv2.COLOR_BGR2RGB)
        # Atualize a imagem exibida na interface gráfica
        atualizar_imagem_exibida(imagem_convertida_rgb)
        # Continue aplicando o filtro em segundo plano
        janela.update()
    # Quando o botão "Confirmar" for pressionado, pare o filtro
    botao_Click = False
    return imagem_convertida_rgb

def aplicar_conversao_cor():
    if vec_of_mats.images:
        # desabilitar botões de filtro
        desabilitar_Botoes()
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = converter_cor(imagem_original)  # Aplique a conversão de cor
        vec_of_mats.images.append(imagem_convertida)  # Armazene a imagem convertida no vetor
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Imagem convertida e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)
        # habilitar botões de filtro
        habilitar_Botoes()



def apply_filter(imagem):
    global trackbar_value, botao_Click
    imagem_convertida_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
    while not botao_Click:
        # Atualize o valor da trackbar (pode ser ajustado)
        trackbar_value = trackbar.get()
        # Certifique-se de que o tamanho do kernel seja ímpar
        if trackbar_value % 2 == 0:
            trackbar_value += 1
            trackbar.set(trackbar_value)
        # Aplique o filtro Gaussian Blur à imagem atual de acordo com o valor da trackbar
        imagem_convertida = cv2.GaussianBlur(imagem_convertida_bgr, (trackbar_value, trackbar_value), 0)
        imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
        # Atualize a imagem exibida na interface gráfica
        atualizar_imagem_exibida(imagem_convertida_rgb)
        # Continue aplicando o filtro em segundo plano
        janela.update()
    # Quando o botão "Confirmar" for pressionado, pare o filtro
    botao_Click = False
    return imagem_convertida_rgb

def aplicar_filtro():
    if vec_of_mats.images:
        # desabilitar botões de filtro
        desabilitar_Botoes()
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = apply_filter(imagem_original)  # Aplique a conversão de cor
        vec_of_mats.images.append(imagem_convertida)  # Armazene a imagem convertida no vetor
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Aplicado o filtro e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)
        # habilitar botões de filtro
        habilitar_Botoes()


def aplicar_detecao(imagem):
    global trackbar_value, botao_Click
    imagem_convertida_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
    while not botao_Click:
        # Atualize o valor da trackbar (pode ser ajustado)
        trackbar_value = trackbar.get()
        # Certifique-se de que o tamanho do kernel seja ímpar
        if trackbar_value % 2 == 0:
            trackbar_value += 1
            trackbar.set(trackbar_value)
        # Aplique o filtro Canny à imagem atual de acordo com o valor da trackbar
        imagem_convertida = cv2.Canny(imagem_convertida_bgr, trackbar_value, trackbar_value*2)
        imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
        # Atualize a imagem exibida na interface gráfica
        atualizar_imagem_exibida(imagem_convertida_rgb)
        # Continue aplicando o filtro em segundo plano
        janela.update()
    # Quando o botão "Confirmar" for pressionado, pare o filtro
    botao_Click = False
    return imagem_convertida_rgb

def detectar_bordas():
    if vec_of_mats.images:
        # desabilitar botões de filtro
        desabilitar_Botoes()
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = aplicar_detecao(imagem_original) # Você pode ajustar os valores 100 e 200 conforme necessário
        vec_of_mats.images.append(imagem_convertida)
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Imagem com bordas detectadas e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)
        # habilitar botões de filtro
        habilitar_Botoes()



def aplicar_binarizacao(imagem):
    global trackbar_value, botao_Click
    imagem_convertida_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
    while not botao_Click:
        # Atualize o valor da trackbar (pode ser ajustado)
        trackbar_value = trackbar.get()
        # Certifique-se de que o tamanho do kernel seja ímpar
        if trackbar_value % 2 == 0:
            trackbar_value += 1
            trackbar.set(trackbar_value)
        # Aplique a binarização da imagem com o uso da trackbar
        _, imagem_convertida = cv2.threshold(imagem_convertida_bgr, trackbar_value, 255, cv2.THRESH_BINARY)
        imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
        # Atualize a imagem exibida na interface gráfica
        atualizar_imagem_exibida(imagem_convertida_rgb)
        # Continue aplicando o filtro em segundo plano
        janela.update()
    # Quando o botão "Confirmar" for pressionado, pare o filtro
    botao_Click = False
    return imagem_convertida_rgb

def binarizar_imagem():
    if vec_of_mats.images:
        # desabilitar botões de filtro
        desabilitar_Botoes()
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = aplicar_binarizacao(imagem_original) # Você pode ajustar os valores 100 e 200 conforme necessário
        vec_of_mats.images.append(imagem_convertida)
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Imagem binarizada e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)
        # habilitar botões de filtro
        habilitar_Botoes()


def apply_morphology(imagem):
    global trackbar_value, botao_Click
    imagem_convertida_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
    while not botao_Click:
        # Atualize o valor da trackbar (pode ser ajustado)
        trackbar_value = trackbar.get()
        # Certifique-se de que o tamanho do kernel seja ímpar
        if trackbar_value % 2 == 0:
            trackbar_value += 1
            trackbar.set(trackbar_value)
        # Aplique a operação de erosão com base no trackbar
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (trackbar_value, trackbar_value))
        imagem_convertida = cv2.erode(imagem_convertida_bgr, kernel, iterations=1)
        imagem_convertida_rgb = cv2.cvtColor(imagem_convertida, cv2.COLOR_BGR2RGB)
        # Atualize a imagem exibida na interface gráfica
        atualizar_imagem_exibida(imagem_convertida_rgb)
        # Continue aplicando o filtro em segundo plano
        janela.update()
    # Quando o botão "Confirmar" for pressionado, pare o filtro
    botao_Click = False
    return imagem_convertida_rgb



def aplicar_morfologia():
    if vec_of_mats.images:
        # desabilitar botões de filtro
        desabilitar_Botoes()
        imagem_original = vec_of_mats.images[-1]  # Obtenha a imagem mais recente do vetor
        imagem_convertida = apply_morphology(imagem_original) # Você pode ajustar os valores 100 e 200 conforme necessário
        vec_of_mats.images.append(imagem_convertida)
        # Atualize a imagem exibida na janela com a imagem de bordas
        print("Aplicada a morfologia e armazenada no vetor.")
        atualizar_imagem_exibida(imagem_convertida)
        # habilitar botões de filtro
        habilitar_Botoes()


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
# Configure o botão "Delete" no frame esquerdo
botao_delete = tk.Button(frame_esquerdo, text="  X  ", width=5, command=delete_imagem)
botao_delete.grid(row=8, column=0, padx=10, pady=10)
# Configure o botão "Confirmar" no frame esquerdo
botao_confirmar = tk.Button(frame_esquerdo, text="Confirmar", width=largura_botoes, command=botao_Confirmar)
botao_confirmar.grid(row=10, column=0, padx=10, pady=10)
# crie uma trackbar dentro do frame_esquerdo
trackbar = tk.Scale(frame_esquerdo, from_=0, to=255, orient="horizontal", length=200)
trackbar.grid(row=9, column=0, padx=10, pady=10)


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