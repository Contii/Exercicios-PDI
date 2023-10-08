import cv2
import os
import random
import numpy as np

def menu_atividade1():
    while True:
        print("===== Menu da Atividade 1 ====")
        print("0 - Voltar ao menu principal")
        print("1 - Realizar ação 1")
        print("2 - Realizar ação 2")
        print("==============================")

        escolha = input("Escolha uma opção: ")

        if escolha == '0':
            break
        elif escolha == '1':
            acao1()
        elif escolha == '2':
            acao2()
        else:
            print("Opção inválida. Tente novamente.")

def acao1():
    print("Executando ação 1 da Atividade 1.")

def acao2():
    print("Executando ação 2 da Atividade 1.")

if __name__ == "__main__":
    menu_atividade1()