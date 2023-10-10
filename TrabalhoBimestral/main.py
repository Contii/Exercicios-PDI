import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from vectorOfMats import VectorOfMats

vec_of_mats = VectorOfMats()

# Função para fechar a janela
def fechar_janela():
    janela.destroy()


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
botao2 = tk.Button(frame_esquerdo, text="convert_color", width=largura_botoes)
botao2.grid(row=1, column=0, padx=10, pady=10)
botao3 = tk.Button(frame_esquerdo, text="apply_filter", width=largura_botoes)
botao3.grid(row=2, column=0, padx=10, pady=10)
botao4 = tk.Button(frame_esquerdo, text="detect_edges", width=largura_botoes)
botao4.grid(row=3, column=0, padx=10, pady=10)
botao5 = tk.Button(frame_esquerdo, text="binarize", width=largura_botoes)
botao5.grid(row=4, column=0, padx=10, pady=10)
botao6 = tk.Button(frame_esquerdo, text="apply_morphology", width=largura_botoes)
botao6.grid(row=5, column=0, padx=10, pady=(10, 40))
botao_salvar = tk.Button(frame_esquerdo, text="Salvar Imagem", width=largura_botoes)
botao_salvar.grid(row=6, column=0, padx=10, pady=10)
# Crie um novo Frame dentro do frame esquerdo para os botões "Next" e "Previous"
frame_botoes_nav = tk.Frame(frame_esquerdo, bg="light gray")
frame_botoes_nav.grid(row=7, column=0, padx=10, pady=10)
# Configure os botões "Next" e "Previous"
botao_previous = tk.Button(frame_botoes_nav, text="  <  ", width=5)
botao_previous.pack(side="left", padx=5)
botao_next = tk.Button(frame_botoes_nav, text="  >  ", width=5)
botao_next.pack(side="left", padx=5)



# Parte direita (80% da largura)
frame_direito = tk.Frame(janela, bg="white")
frame_direito.grid(row=0, column=1, sticky="nsew")
# Crie um novo Frame dentro do frame_direito para a imagem
frame_imagem = tk.Frame(frame_direito)
frame_imagem.pack(fill="both", expand=True)
# Crie um Label para exibir a imagem
label_imagem = tk.Label(frame_imagem)
label_imagem.pack(fill="both", expand=True)



# Configure o botão para fechar a janela
janela.protocol("WM_DELETE_WINDOW", fechar_janela)
# Use o weight para que as colunas se expandam com o redimensionamento da janela
janela.mainloop()