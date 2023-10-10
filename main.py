import os

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
    trabalhoBimestral.front()


if __name__ == "__main__":
    main()