import os
import cv2
import numpy as np

import Atividade1_Canais_de_cores.canaisDeCores as exercicio1
import Atividade2_HighGUI.highGUI as exercicio2
import Atividade3_GalinhasEBocha.bocha as exercicio3_1
import Atividade3_GalinhasEBocha.galinhas as exercicio3_2
import TrabalhoBimestral.main as trabalhoBimestral

def main():
    while True:
        os.system('cls')
        print("= = Universidade Tecnológica Federal do Parana - Campus Medianeira. = =")
        print(" = = = = Processamento de Imagens e Reconhecimento de padroes. = = = = ")
        print("= = = = = = = = = = = = = = Joao Vitor Conti. = = = = = = = = = = = = =") 
        print()
        print("=============== Menu das Atividades ==============")
        print(" 1 - Exercicio 1 - Canais de Cores.")
        print(" 2 - Exercicio 2 - HighGUI.")
        print(" 3 - Exercicio 3 - Binarização e Contagem.")
        print(" 4 - Trabalho Bimestral 1.")
        print(" 0 - Sair.")
        print("==================================================")

        escolha = input("Escolha uma opção: ")

        if escolha == '0':
            break
        elif escolha == '1':
            os.system('cls')
            acao1()
        elif escolha == '2':
            os.system('cls')
            acao2()
        elif escolha == '3':
            os.system('cls')
            acao3()
        elif escolha == '4':
            os.system('cls')
            acao4()
        else:
            print("Opção inválida. Tente novamente.")

def acao1():
    print("================== Atividade 1 ===================")
    exercicio1.canaisDeCores()

def acao2():
    print("================== Atividade 2 ===================")
    exercicio2.highGUI()

def acao3():
    while True:
        os.system('cls')
        print("============== Menu da Atividade 3 ===============")
        print(" 1 - Exercicio 1 - Binarizar Bocha.")
        print(" 2 - Exercicio 2 - Contar Galinhas.")
        print(" 0 - Sair.")
        print("==================================================")
        escolha2 = input("Escolha uma opção: ")

        if escolha2 == '0':
            break
        elif escolha2 == '1':
            exercicio3_1.bocha()
        elif escolha2 == '2':
            os.system('cls')
            print("===== Exercicio 2 - Contar Galinhas. =====")
            print("Este exercicio ainda nao foi implementado.")
            #exercicio3_2()
            input("Pressione qualquer tecla para continuar...")
            
        else:
            print("Opção inválida. Tente novamente")

def acao4():
    # Crie uma instância da classe VectorOfMats
    vector = trabalhoBimestral.VectorOfMats()

    # Adicione imagens ao vetor
    vector.add_image('Media/Lenna.png')
    vector.add_image('Media/bocha.JPG')
    vector.add_image('Media/galinha.png')
    vector.add_image('Media/borboleta.jpg')

    # Função para exibir o menu principal
    def exibir_menu():
        os.system('cls')
        print("==================== Trabalho Bimestral 1. ====================")
        print("1: Escolher imagem")
        print("2: Tratar imagem")
        print("3: Salvar imagem")
        print("0: Sair")

    # Loop principal
    while True:
        exibir_menu()
        escolha = input("Digite o número da opção desejada: ")

        if escolha == '0':
            break
        elif escolha == '1':
            print("==============================================================")
            print("============= Escolha uma imagem para trabalhar: =============")
            for i, image in enumerate(vector.images):
                print(f"{i + 1}: Imagem {i + 1}")
            print("0: Voltar ao menu principal")

            escolha_imagem = input("Digite o número da imagem: ")
            if escolha_imagem == '0':
                continue

            try:
                escolha_imagem = int(escolha_imagem) - 1
                if 0 <= escolha_imagem < len(vector.images):
                    print(f"Imagem {escolha_imagem + 1} selecionada.")
                    input("Pressione qualquer tecla para continuar...")
                else:
                    print("Escolha inválida. Por favor, escolha um número de imagem válido.")
            except ValueError:
                print("Escolha inválida. Por favor, digite um número válido.")

        elif escolha == '2':
            if not vector.images:
                print("Por favor, adicione pelo menos uma imagem antes de tratar.")
            else:
                if 'escolha_imagem' not in locals():
                    print("Por favor, escolha uma imagem antes de continuar.")
                    continue

                imagem = vector.images[escolha_imagem]

                # Menu para tratar a imagem
                while True:
                    print("==============================================================")
                    print("==================== Menu de Tratamento: =====================")
                    print("1: Conversão de cor")
                    print("2: Aplicar filtro")
                    print("3: Detectar bordas")
                    print("4: Binarizar imagem")
                    print("5: Aplicar morfologia matemática")
                    print("0: Voltar ao menu principal")

                    escolha_tratamento = input("Digite o número do tratamento: ")

                    if escolha_tratamento == '0':
                        break
                    elif escolha_tratamento == '1':
                        color_conversion = int(input("Digite o código de conversão de cor (por exemplo, digite 6 para cv2.COLOR_BGR2GRAY): "))
                        vector.convert_color(escolha_imagem, color_conversion)
                    elif escolha_tratamento == '2':
                        # Implemente a lógica para aplicar filtro aqui
                        pass
                    elif escolha_tratamento == '3':
                        low_threshold = int(input("Digite o limite inferior para detecção de bordas: "))
                        high_threshold = int(input("Digite o limite superior para detecção de bordas: "))
                        vector.detect_edges(escolha_imagem, low_threshold, high_threshold)
                    elif escolha_tratamento == '4':
                        threshold = int(input("Digite o valor de threshold: "))
                        vector.binarize(escolha_imagem, threshold)
                    elif escolha_tratamento == '5':
                        operation = input("Digite a operação de morfologia matemática (dilate ou erode): ")
                        kernel_size = int(input("Digite o tamanho do kernel: "))
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
                        vector.apply_morphology(escolha_imagem, operation, kernel)
                    else:
                        print("Escolha inválida. Por favor, digite um número de tratamento válido.")

        elif escolha == '3':
            if not vector.images:
                print("Por favor, adicione pelo menos uma imagem antes de salvar.")
            else:
                output_folder = input("Digite o nome da pasta de saída: ")
                vector.save_images(output_folder)
                print(f"Imagens salvas na pasta '{output_folder}'.")
                input("Pressione qualquer tecla para continuar...")

        else:
            print("Escolha inválida. Por favor, digite um número de opção válido.")


if __name__ == "__main__":
    main()