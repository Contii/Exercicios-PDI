import cv2

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def blur(image):
    return cv2.GaussianBlur(image, (15, 15), 0)

def edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return edges

def main():
    print("===============================================================")
    print("Este exercício faz um tratamento em uma imagem da pasta Media.")
    image_name = input("Digite o nome da imagem (exemplo: Lenna.png): ")
    image_path = f'../Media/{image_name}'
    image = cv2.imread(image_path)

    if image is None:
        print("Erro ao carregar a imagem. Verifique o nome do arquivo.")
        return
    
    while True:
        print("Menu de Opções:")
        print("1. Escala de Cinza")
        print("2. Desfoque")
        print("3. Detecção de Bordas")
        print("4. Sair")
        choice = int(input("Escolha uma opção: "))

        if choice == 1:
            processed_image = grayscale(image)
        elif choice == 2:
            processed_image = blur(image)
        elif choice == 3:
            processed_image = edge_detection(image)
        elif choice == 4:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue

        cv2.imshow('Processed Image', processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()