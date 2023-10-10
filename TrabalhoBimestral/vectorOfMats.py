import os
import cv2

class VectorOfMats:
    def __init__(self):
        self.images = []  # Lista para armazenar as imagens
        self.image_names = []  # Lista para armazenar os nomes dos arquivos das imagens

    # Adicione uma imagem à lista de imagens
    def add_image(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            self.images.append(image)
            self.image_names.append(os.path.basename(image_path))  # Armazene o nome do arquivo
            return True
        else:
            return False
    
    # salve a imagem que for fornecida como parâmetro na pasta folder_path como .jpg
    def save_image(self, index, folder_path, new_image_name):
        if 0 <= index < len(self.images):
            image_path = os.path.join(folder_path, new_image_name + '.jpg')
            cv2.imwrite(image_path, self.images[index])



    # converte a imagem para outro espaço de cores
    def convert_color(self, index, color_conversion):
        if 0 <= index < len(self.images):
            self.images[index] = cv2.cvtColor(self.images[index], color_conversion)

    # aplica um filtro à imagem
    def apply_filter(self, index, kernel):
        if 0 <= index < len(self.images):
            self.images[index] = cv2.filter2D(self.images[index], -1, kernel)

    # detecta bordas na imagem em escala de cinza
    def detect_edges(self, index, low_threshold, high_threshold):
        if 0 <= index < len(self.images):
            gray = cv2.cvtColor(self.images[index], cv2.COLOR_BGR2GRAY)
            self.images[index] = cv2.Canny(gray, low_threshold, high_threshold)

    # binarize a imagem em escala de cinza
    def binarize(self, index, threshold):
        if 0 <= index < len(self.images):
            gray = cv2.cvtColor(self.images[index], cv2.COLOR_BGR2GRAY)
            _, binary_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            self.images[index] = binary_img

    # aplica uma operação de morfologia matemática à imagem
    def apply_morphology(self, index, operation, kernel):
        if 0 <= index < len(self.images):
            if operation == 'dilate':
                self.images[index] = cv2.dilate(self.images[index], kernel, iterations=1)
            elif operation == 'erode':
                self.images[index] = cv2.erode(self.images[index], kernel, iterations=1)



# Exemplo de uso
if __name__ == '__main__':
    vec_of_mats = VectorOfMats()


    # Adicione todas as imagens .jpg e .png de uma pasta ao vetor
    folder_path = 'Media'  # Substitua pelo caminho da pasta desejada
    vec_of_mats.add_images_from_folder(folder_path)

    # liste e peça para selecionar uma imagem
    index = vec_of_mats.select_image()
    # exiba somente a imagem selecionada
    cv2.imshow("Imagem selecionada", vec_of_mats.images[index])
    cv2.waitKey(0)

    # pergunte o nome da nova imagem
    new_image_name = input("Digite o nome da nova imagem: ")
    # salve a imagem selecionada na pasta folder_path
    vec_of_mats.save_image(index, folder_path, new_image_name)

    # reinicie o vetor de imagens com todas as imagens da pasta folder_path
    vec_of_mats.reset(folder_path)

    # liste e peça para selecionar uma imagem
    index = vec_of_mats.select_image()
    print(index)

    





    # # # Adicione imagens ao vetor
    # vec_of_mats.add_image('../Media/Lenna.png')
    # vec_of_mats.add_image('../Media/bocha.JPG')
    # vec_of_mats.add_image('../Media/galinha.png')
    # vec_of_mats.add_image('../Media/borboleta.jpg')

    # # Converta a primeira imagem para escala de cinza
    # vec_of_mats.convert_color(0, cv2.COLOR_BGR2GRAY)

    # # Aplique um filtro à segunda imagem
    # kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]], dtype=np.float32)
    # vec_of_mats.apply_filter(1, kernel)

    # # Detecte bordas na primeira imagem
    # vec_of_mats.detect_edges(1, 100, 200)

    # # Binarize a quarta imagem
    # vec_of_mats.binarize(4, 128)

    # # Aplique morfologia matemática de dilatação na segunda imagem
    # kernel = np.ones((5, 5), np.uint8)
    # vec_of_mats.apply_morphology(2, 'dilate', kernel)

    # # Salve as imagens processadas
    # vec_of_mats.save_images('../Media')